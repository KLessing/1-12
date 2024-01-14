import bpy
import math

dice = bpy.data.objects['Cube']
start_frame = 1
end_frame = 180
roll_count = 2

# 180 x z = 1
# 270 x y = 2
# 270 x z = 3
# 90 x z = 4
# 90 x y = 5
# 0 / 180 / 360 x y = 6 

# reset rotations
dice.rotation_euler.x = 0
dice.rotation_euler.y = 0
dice.rotation_euler.z = 0
# insert keyframe at frame one
dice.keyframe_insert("rotation_euler", frame=start_frame)

# change the rotation of the cube
# (negative to roll "away")
degrees = 270 + (360 * roll_count)
radians = math.radians(degrees)
dice.rotation_euler.x = -radians
#dice.rotation_euler.y = -radians
dice.rotation_euler.z = -radians

# insert keyframe at the last frame
dice.keyframe_insert("rotation_euler", frame=end_frame)

# generate images from animation
# TODO set Frame Range Set in Camera object Accordingly
#bpy.context.scene.render.filepath = ("C:\\Projects\\1-12\\blender\\images\\img")
#bpy.ops.render.render(animation=True, write_still=True)
