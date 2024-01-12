import bpy

dice = bpy.data.objects['Cube']
dice.rotation_axis_angle = [90.0, 1.0, 0.0, 0.0]

bpy.context.scene.render.filepath = ("C:\\Projects\\1-12\\blender\\images\\img")
bpy.ops.render.render( animation=True, write_still=True ) 