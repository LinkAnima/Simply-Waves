import maya.cmds as cmds
import maya.api.OpenMaya as om
import traceback
import random
import math

# =============================================================================
# CONFIGURATION
# =============================================================================
RIG_NAME_PREFIX = "simply_waves_rig"
JOINT_PREFIX = "simply_waves_joint_"

# =============================================================================
# CORE FUNCTIONS
# =============================================================================
def create_plane_mesh(width, height, sub_x, sub_y, poly_type='quad'):
    """Creates the base polygon plane."""
    print(f"[*] Creating plane: {width}x{height}, {sub_x}x{sub_y}, {poly_type}")
    
    # Input validation
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive")
    if sub_x < 1 or sub_y < 1:
        raise ValueError("Subdivision counts must be at least 1")
    
    try:
        cmds.select(cl=True)
        
        mesh_name = cmds.polyPlane(
            w=width, h=height, sx=sub_x, sy=sub_y,
            ax=[0, 1, 0], cuv=2, ch=1
        )[0]
        
        if poly_type == 'triangle':
            cmds.polyTriangulate(mesh_name)
            
        return mesh_name
    except Exception as e:
        raise RuntimeError(f"Failed to create plane: {e}")

def create_joint_grid(mesh_name):
    """Creates a joint at every vertex using OpenMaya API 2.0 for speed."""
    print("[*] Creating joint grid...")
    
    # Input validation
    if not mesh_name or not cmds.objExists(mesh_name):
        raise ValueError("Invalid mesh name provided")
    
    try:
        sel = om.MSelectionList()
        sel.add(mesh_name)
        dag_path = sel.getDagPath(0)
        mesh_fn = om.MFnMesh(dag_path)
        
        num_verts = mesh_fn.numVertices
        points = mesh_fn.getPoints(om.MSpace.kWorld)
        
        joints = []
        for i in range(num_verts):
            pos = points[i]
            joint_name = f"{JOINT_PREFIX}_{i:04d}"
            cmds.joint(p=(pos.x, pos.y, pos.z), n=joint_name)
            joints.append(joint_name)
            
        print(f"[*] Created {len(joints)} joints.")
        return joints
    except Exception as e:
        raise RuntimeError(f"Failed to create joints: {e}")

def bind_skin_optimized(mesh_name, joints):
    """Binds mesh to joints using cmds.skinCluster and cmds.skinPercent."""
    print("[*] Binding skin cluster...")
    
    # Input validation
    if not mesh_name or not joints:
        raise ValueError("Invalid mesh name or joints list")
    
    try:
        cmds.select(mesh_name, joints)
        skin_cluster = cmds.skinCluster(bindMethod=0, maximumInfluences=1)[0]
        
        for i, joint_name in enumerate(joints):
            cmds.skinPercent(
                skin_cluster, 
                f"{mesh_name}.vtx[{i}]", 
                transformValue=[(joint_name, 1.0)]
            )
            
        print("[*] Skin binding complete.")
        cmds.select(cl=True)
    except Exception as e:
        raise RuntimeError(f"Failed to bind skin: {e}")

def setup_animation(mesh_name, joints, width, height, amplitude, speed, num_layers, frame_count, frame_rate):
    """Sets up procedural wave animation using expressions with adjustable layers."""
    print(f"[*] Setting up animation with {num_layers} wave layers...")
    
    # Input validation
    if not joints or len(joints) == 0:
        raise ValueError("No joints provided for animation")
    
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive")
    
    # 1. Get Mesh Center for Offset Calculation
    center_pos = cmds.xform(mesh_name, q=True, ws=True, rp=True)
    cx, cy, cz = center_pos
    
    # 2. Generate Dynamic Expression String
    # We will build the sine terms dynamically based on num_layers
    
    # Base expression header
    expr_header = """
// Simply Waves Expression for {joint}
float $speed = {speed};
float $amp = {amplitude};
float $t = time * $speed;
float $w = {width};
float $h = {height};
float $rx = `getAttr {joint}.restX`;
float $rz = `getAttr {joint}.restZ`;
float $totalDY = 0;
"""
    
    # Generate Sine Terms for each layer
    # We use different frequency multipliers and phase shifts for variety
    expr_body = ""
    
    # Build wave layers efficiently
    for layer in range(num_layers):
        # Calculate frequency multipliers
        freq_mult_x = 2 ** (layer) 
        freq_mult_y = 2 ** (layer)
        
        # More precise wave math with proper handling of zero dimensions
        kx = math.pi * freq_mult_x / width if width > 0 else 0
        ky = math.pi * freq_mult_y / height if height > 0 else 0
        
        # Phase shift to make waves move diagonally or organically
        phase_shift = (layer + 1) * 1.5 
        
        # Amplitude decay: Higher layers have less impact
        amp_factor = 1.0 / (layer + 1)
        
        # Construct the sine term
        term = f"""
// Layer {layer}
float $dy{layer} = $amp * {amp_factor:.6f} * sin({kx:.6f} * $rx + {ky:.6f} * $rz + {phase_shift:.6f} * $t);
$totalDY += $dy{layer};
"""
        expr_body += term
        
    # Final assignment
    expr_footer = """
setAttr {joint}.translateY $totalDY;
"""
    
    full_expr_template = expr_header + expr_body + expr_footer
    
    # 3. Apply Expressions to Joints
    for i, j_name in enumerate(joints):
        pos = cmds.joint(j_name, q=True, p=True)
        
        ox = pos[0] - cx
        oz = pos[2] - cz
        
        # Store rest positions as attributes
        if not cmds.attributeQuery('restX', node=j_name, ex=True):
            cmds.addAttr(j_name, ln='restX', at='double', dv=ox, keyable=False)
            cmds.addAttr(j_name, ln='restZ', at='double', dv=oz, keyable=False)
            
        # Replace placeholders
        expr_str = full_expr_template.replace("{speed}", str(speed))
        expr_str = expr_str.replace("{amplitude}", str(amplitude))
        expr_str = expr_str.replace("{width}", str(width))
        expr_str = expr_str.replace("{height}", str(height))
        expr_str = expr_str.replace("{joint}", j_name)
        
        expr_name = f"expr_{j_name}"
        if cmds.objExists(expr_name):
            try:
                cmds.delete(expr_name)
            except Exception:
                pass
            
        try:
            cmds.expression(s=expr_str, n=expr_name)
        except Exception as e:
            print(f"Warning: Failed to create expression for {j_name}: {e}")
            
    print("[*] Animation setup complete.")

def generate_ocean_rig(width, height, sub_x, sub_y, poly_type, amplitude, speed, num_layers, frame_count, frame_rate):
    """Main orchestration function."""
    print("="*30)
    print("Starting Simply Waves Generation")
    print("="*30)
    
    try:
        # Clean up any existing rigs with same name
        to_delete = []
        all_objects = cmds.ls(RIG_NAME_PREFIX + "*", type="transform")
        
        # Also look for joint groups or other related objects
        for obj in all_objects:
            if "joint" in obj.lower() or "control" in obj.lower():
                to_delete.append(obj)
        
        # Delete everything at once for better performance
        if to_delete:
            try:
                cmds.delete(to_delete)
            except Exception:
                pass
        
        mesh_name = create_plane_mesh(width, height, sub_x, sub_y, poly_type)
        
        # Make sure the mesh is properly positioned
        cmds.select(mesh_name)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        
        joints = create_joint_grid(mesh_name)
        bind_skin_optimized(mesh_name, joints)
        setup_animation(mesh_name, joints, width, height, amplitude, speed, num_layers, frame_count, frame_rate)
        
        # Create and organize the rig group
        rig_group = cmds.group(em=True, n=RIG_NAME_PREFIX)
        cmds.parent(mesh_name, rig_group)
        for j in joints:
            cmds.parent(j, rig_group)
            
        print("="*30)
        print("Simply Waves Generation Successful!")
        print("="*30)
        
        cmds.select(RIG_NAME_PREFIX)
        
        # Auto-play - Extended to specified frame count
        try:
            cmds.playbackOptions(min=1, max=frame_count, ast=1, aet=frame_count)
            cmds.currentTime(1, edit=True)
            cmds.play()
        except Exception:
            pass
        
    except Exception as e:
        print("="*30)
        print("ERROR: Simply Waves generation failed.")
        print("="*30)
        print(traceback.format_exc())
        raise e

def delete_ocean_rig(*args):
    """Completely deletes the simply waves rig."""
    try:
        # Find all objects with the exact rig prefix
        rig_group = cmds.ls(RIG_NAME_PREFIX, type="transform")
        
        if rig_group:
            # Delete the entire rig group and its contents
            cmds.delete(rig_group)
            print("[*] Simply Waves rig deleted successfully.")
            cmds.inViewMessage(amg="Simply Waves Rig Deleted Successfully!", fade=True, fadeStayTime=1)
        else:
            # Try to find objects that might match our pattern
            all_objects = cmds.ls(RIG_NAME_PREFIX + "*", type="transform")
            if all_objects:
                cmds.delete(all_objects)
                print("[*] Simply Waves rig elements deleted successfully.")
                cmds.inViewMessage(amg="Simply Waves Rig Elements Deleted Successfully!", fade=True, fadeStayTime=1)
            else:
                print("[*] No Simply Waves rig found to delete.")
                cmds.inViewMessage(amg="No Simply Waves Rig Found to Delete", fade=True, fadeStayTime=1)
            
    except Exception as e:
        print(f"[*] Error deleting Simply Waves rig: {e}")
        traceback.print_exc()
        cmds.inViewMessage(amg="Error deleting Simply Waves rig. See Script Editor.", fade=True, fadeStayTime=2)

# =============================================================================
# UI SETUP
# =============================================================================
def create_ui():
    window_name = "SimplyWavesWindow"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
        
    window = cmds.window(window_name, title="Simply Waves", widthHeight=(300, 600))
    
    cmds.columnLayout(adj=True)
    cmds.separator(h=10)
    
    cmds.text("Geometry Settings")
    cmds.separator(h=5)
    
    cmds.text("Width:")
    width_field = cmds.floatField(v=10.0, precision=2, min=0.1)
    
    cmds.text("Height:")
    height_field = cmds.floatField(v=10.0, precision=2, min=0.1)
    
    cmds.text("Subdivisions X:")
    sub_x_field = cmds.intField(v=10, min=1)
    
    cmds.text("Subdivisions Y:")
    sub_y_field = cmds.intField(v=10, min=1)
    
    cmds.text("Polygon Type:")
    poly_type_menu = cmds.optionMenu(label="Poly Type")
    cmds.menuItem(label="Quads")
    cmds.menuItem(label="Triangles")
    
    cmds.separator(h=10)
    cmds.text("Wave Physics")
    cmds.separator(h=5)
    
    amp_field = cmds.floatSliderGrp(l="Amplitude", field=True, v=0.5, min=0, max=2)
    speed_field = cmds.floatSliderGrp(l="Speed", field=True, v=1.0, min=0.1, max=5)
    
    # NEW: Wave Layers Input
    cmds.text("Wave Layers (Complexity):")
    layers_field = cmds.intField(v=3, min=1, max=10)
    
    cmds.separator(h=10)
    cmds.text("Animation Settings")
    cmds.separator(h=5)
    
    # Frame count control
    cmds.text("Frame Count:")
    frame_count_field = cmds.intField(v=240, min=1, max=1000)
    
    # Frame rate control
    cmds.text("Frame Rate (fps):")
    frame_rate_field = cmds.intField(v=24, min=1, max=120)
    
    cmds.separator(h=20)
    
    def on_generate(*args):
        # Validate inputs before processing
        try:
            w = cmds.floatField(width_field, q=True, v=True)
            h = cmds.floatField(height_field, q=True, v=True)
            sx = cmds.intField(sub_x_field, q=True, v=True)
            sy = cmds.intField(sub_y_field, q=True, v=True)
            amp = cmds.floatSliderGrp(amp_field, q=True, v=True)
            spd = cmds.floatSliderGrp(speed_field, q=True, v=True)
            layers = cmds.intField(layers_field, q=True, v=True)
            frame_count = cmds.intField(frame_count_field, q=True, v=True)
            frame_rate = cmds.intField(frame_rate_field, q=True, v=True)
            
            # Validate inputs
            if w <= 0 or h <= 0:
                raise ValueError("Width and height must be positive")
            if sx < 1 or sy < 1:
                raise ValueError("Subdivisions must be at least 1")
            if layers < 1 or layers > 10:
                raise ValueError("Wave layers must be between 1 and 10")
            if frame_count < 1 or frame_count > 1000:
                raise ValueError("Frame count must be between 1 and 1000")
            if frame_rate < 1 or frame_rate > 120:
                raise ValueError("Frame rate must be between 1 and 120")
            
            cmds.button(btn_gen, e=True, enable=False)
            
            # Get polygon type
            poly_label = cmds.optionMenu(poly_type_menu, q=True, v=True)
            poly_type = 'triangle' if poly_label == "Triangles" else 'quad'
            
            # Generate with better error handling
            generate_ocean_rig(w, h, sx, sy, poly_type, amp, spd, layers, frame_count, frame_rate)
            cmds.inViewMessage(amg="Simply Waves Created Successfully!", fade=True, fadeStayTime=1)
            
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            cmds.inViewMessage(amg="Error occurred. See Script Editor for details", fade=True, fadeStayTime=2)
        finally:
            cmds.button(btn_gen, e=True, enable=True)
    
    btn_gen = cmds.button(label="Generate Simply Waves", command=on_generate, h=50, ann="Click to generate the waves")
    
    # NEW: Delete Button
    cmds.separator(h=10)
    delete_btn = cmds.button(label="Delete Simply Waves Rig", command=delete_ocean_rig, h=30, 
                            ann="Completely delete the current Simply Waves rig")
    
    cmds.separator(h=10)
    cmds.text("Note: Higher layers = more complex waves but slower eval.")
    cmds.text("Note: Frame count determines animation duration (Frame Count / FPS = seconds)")
    
    cmds.showWindow(window)

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    create_ui()
