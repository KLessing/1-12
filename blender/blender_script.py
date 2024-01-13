import bpy
import math
from math import radians


dice = bpy.data.objects['Cube']

bpy.context.view_layer.objects.active = dice
# TODO research select by name 
bpy.ops.object.select_by_type(extend=False, type='MESH')

#dice.rotation_axis_angle = [0.0, 0.0, 1.0, radians(90)]
#dice.rotation_axis_angle = [45.0, 1.0, 0.0, 0.0]
#dice.rotation_axis_angle = [180.0, 1.0, 0.0, 0.0]
#dice.rotation_axis_angle = [1.0, 1.0, 1.0, 45.0]

# insert keyframe at frame one
start_frame = 1
dice.keyframe_insert("rotation_euler", frame=start_frame)

# change the rotation of the cube around z-axis
degrees = 90
radians = math.radians(degrees)
dice.rotation_euler.z = radians

# insert keyframe at the last frame
end_frame = 180
dice.keyframe_insert("rotation_euler", frame=end_frame)


#bpy.context.scene.render.filepath = ("C:\\Projects\\1-12\\blender\\images\\img")
#bpy.ops.render.render(animation=True, write_still=True)
