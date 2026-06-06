# Simply Waves User Guide

Welcome to Simply Waves! This powerful Maya tool helps you create beautiful, realistic ocean wave animations with minimal effort. Whether you're a beginner or experienced artist, this guide will help you get the most out of Simply Waves.

## What is Simply Waves?

Simply Waves is a Maya plugin that generates procedural ocean waves using mathematical wave equations. Instead of manually animating each vertex, it automatically creates wave patterns that look natural and dynamic. The tool works by:
- Creating a mesh plane with adjustable dimensions
- Placing joints at every vertex of the mesh
- Using mathematical expressions to animate the joints in wave patterns
- Giving you full control over wave characteristics

## Getting Started

### Launching the Tool
1. Open Maya
2. In the Script Editor, paste the Simply Waves script
3. Run the script (press Ctrl+A then Ctrl+Enter)
4. The "Simply Waves" window will appear

### Basic Workflow
1. Set your desired parameters in the UI
2. Click "Generate Simply Waves"
3. Watch as your ocean waves animate automatically
4. Use the "Delete Simply Waves Rig" button to clean up when needed

## Understanding the Controls

### Geometry Settings
- **Width & Height**: Sets how large your wave plane is
- **Subdivisions X & Y**: Controls how many vertices make up your mesh (more = smoother waves)
- **Polygon Type**: Choose between Quads (faster) or Triangles (more detailed)

### Wave Physics
- **Amplitude**: How high the waves go (0 = flat, higher = more dramatic waves)
- **Speed**: How fast the waves move (0.1 = slow, higher = faster waves)
- **Wave Layers**: Number of wave patterns layered together (1 = simple, 10 = very complex)

### Animation Settings
- **Frame Count**: Total number of frames in your animation (1-1000)
- **Frame Rate**: How many frames per second (1-120 fps)

## Best Practices

### For Beginners
1. **Start Simple**: Begin with 3-5 wave layers, low amplitude, and moderate speed
2. **Test First**: Generate a small test rig to see how parameters affect your waves
3. **Use Reasonable Dimensions**: Start with 10x10 units for width and height

### For Advanced Users
1. **Layer Complexity**: Use more layers (5-10) for complex, natural-looking waves
2. **Frame Rate Considerations**: 
   - 24 fps = cinematic quality (good for most animations)
   - 30 fps = TV/film standard
   - Higher frame rates = smoother motion but slower evaluation
3. **Frame Count Planning**:
   - For a 5-second animation at 24 fps: 120 frames
   - For a 10-second animation at 24 fps: 240 frames

### Performance Tips
- **Fewer Subdivisions**: Use lower subdivisions (8x8) for faster preview
- **Less Layers**: Start with 3 layers, increase only if needed
- **Shorter Animations**: For quick previews, use 60-120 frames instead of 240+
- **High Frame Rates**: Only use 60+ fps if you need very smooth motion

## Using the Animation Controls

### Wave Parameters Explained
**Amplitude (Height)**:
- Low values (0.1-0.3): Gentle ripples, small waves
- Medium values (0.5-1.0): Normal ocean waves
- High values (1.5+): Dramatic, stormy waves

**Speed (Motion)**:
- Slow speeds (0.2-0.5): Calm ocean, gentle movement
- Medium speeds (1.0-2.0): Regular ocean conditions
- Fast speeds (3.0+): Stormy or turbulent water

**Wave Layers**:
- 1 layer: Single wave pattern
- 3 layers: Natural-looking waves with some complexity
- 5-7 layers: Realistic ocean with multiple wave systems
- 10 layers: Very complex, detailed wave patterns (use carefully)

## Troubleshooting Common Issues

### Issue 1: Joints Not Moving with Mesh
**Problem**: The wave animation looks like the mesh is moving but joints aren't following.
**Solution**: 
1. Try deleting the current rig using "Delete Simply Waves Rig"
2. Generate a new rig with fewer subdivisions (8x8) first
3. Ensure you're playing back in the correct time range

### Issue 2: Tool Not Working After First Use
**Problem**: After generating and deleting, subsequent generations don't work properly.
**Solution**:
1. Always use the "Delete Simply Waves Rig" button between runs
2. If problems persist, restart Maya completely
3. Check that no objects with "simply_waves_rig" exist in your scene

### Issue 3: Slow Performance
**Problem**: The tool runs very slowly or causes Maya to freeze.
**Solution**:
1. Reduce subdivisions (try 8x8 instead of 20x20)
2. Lower wave layers (start with 3 instead of 10)
3. Use fewer frames in your animation
4. Increase frame rate to reduce evaluation time

## Customizing Your Waves

### Creating Different Wave Types
**Gentle Ocean**: 
- Amplitude: 0.3
- Speed: 0.5
- Layers: 3
- Subdivisions: 10x10

**Stormy Sea**:
- Amplitude: 1.5
- Speed: 2.0
- Layers: 7
- Subdivisions: 15x15

**Rippling Ponds**:
- Amplitude: 0.1
- Speed: 0.2
- Layers: 2
- Subdivisions: 8x8

### Advanced Settings
- **Frame Count**: For a 5-second animation at 24 fps, use 120 frames
- **Frame Rate**: Use 24 fps for most projects, 30 fps for video editing
- **Polygon Type**: Quads are faster; triangles give more detail

## Scene Management

### Working with Multiple Rigs
Simply Waves automatically cleans up any existing rigs before creating new ones. However:
1. If you want to keep multiple wave systems, rename the rig group before generating a new one
2. Use "Delete Simply Waves Rig" button to remove current system
3. Don't manually delete objects - always use the tool's delete function

### Integration with Other Tools
- Simply Waves works well with Maya's built-in rendering engines (Arnold, Redshift)
- Can be used for animation, simulation, or as a reference for other effects
- Combine with other ocean tools by layering multiple wave systems

## Tips for Professional Results

1. **Use the Preview**: Always generate a quick test before full production
2. **Layer Your Waves**: Combine multiple wave systems for more realism
3. **Match Your Scene**: Adjust parameters to match your specific environment
4. **Save Often**: Use Maya's save functionality during development
5. **Optimize for Performance**: Balance quality with speed requirements

## Common Workflow Patterns

### Quick Test Setup:
1. Set width/height to 10x10
2. Use 8x8 subdivisions 
3. Amplitude: 0.5, Speed: 1.0, Layers: 3
4. Frame count: 60, Frame rate: 24
5. Generate and preview

### Production Setup:
1. Set width/height to your scene requirements
2. Use 15x15 or higher subdivisions for detailed waves
3. Adjust amplitude/speed based on desired effect
4. Use 5-7 layers for realistic ocean
5. Frame count: 240+ for full animation, frame rate: 24

### Cleanup Process:
1. When done with your wave animation
2. Click "Delete Simply Waves Rig" button
3. Verify no objects remain with "simply_waves_" prefix
4. Continue with other scene work

## Support and Feedback

Simply Waves is designed to be intuitive, but if you encounter any issues:
- Check that Maya is running properly
- Ensure your system meets minimum requirements
- Restart Maya if problems persist
- Contact support if you have specific feature requests

Remember, the key to great waves is experimentation. Start simple, then gradually increase complexity until you achieve the look you want!

Happy animating! 🌊
