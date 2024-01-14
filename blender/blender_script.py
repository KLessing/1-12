import bpy
import math

dice = bpy.data.objects['Cube']

# reset rotations
dice.rotation_euler.x = 0
dice.rotation_euler.y = 0
dice.rotation_euler.z = 0

# insert keyframe at frame one
start_frame = 1
dice.keyframe_insert("rotation_euler", frame=start_frame)

# change the rotation of the cube
degrees = 360
radians = math.radians(degrees)
dice.rotation_euler.x = radians
dice.rotation_euler.y = radians
dice.rotation_euler.z = radians

# insert keyframe at the last frame
end_frame = 180
dice.keyframe_insert("rotation_euler", frame=end_frame)

# generate images from animation
# TODO set Frame Range Set in Camera object Accordingly
#bpy.context.scene.render.filepath = ("C:\\Projects\\1-12\\blender\\images\\img")
#bpy.ops.render.render(animation=True, write_still=True)
