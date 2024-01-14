import bpy
import math

dice = bpy.data.objects['Cube']
start_frame = 1
end_frame = 180
roll_count = 2

# Degree y z by index
rolls = [
    [180, False, True],
    [270, True, False],
    [270, False, True],
    [90, False, True],
    [90, True, False],
    [180, True, False],
]

def reset_rotation_values():
    dice.rotation_euler.x = 0
    dice.rotation_euler.y = 0
    dice.rotation_euler.z = 0
    # insert keyframe at frame one
    dice.keyframe_insert("rotation_euler", frame=start_frame)

def animate_roll(degree: int, count: int, y: bool, z: bool):
    # change the rotation of the cube
    # (negative to roll "away")
    degrees = degree + (360 * count)
    radians = math.radians(degrees)

    dice.rotation_euler.x = -radians
    dice.rotation_euler.y = -radians if y else 0
    dice.rotation_euler.z = -radians if z else 0

    # insert keyframe at the last frame
    dice.keyframe_insert("rotation_euler", frame=end_frame)

i = 5
reset_rotation_values()
animate_roll(rolls[i][0], roll_count, rolls[i][1], rolls[i][2])

# generate images from animation
# TODO set Frame Range Set in Camera object Accordingly
#bpy.context.scene.render.filepath = ("C:\\Projects\\1-12\\blender\\images\\img")
#bpy.ops.render.render(animation=True, write_still=True)
