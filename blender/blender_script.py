import bpy
import math

PARENT_PATH = "C:\\Projects\\1-12\\blender\\images\\"
dice = bpy.data.objects['Cube']
roll_count = 1

# set frame range for 16 images in 10 steps
start_frame = 1
end_frame = 151

bpy.context.scene.frame_start = start_frame
bpy.context.scene.frame_end = end_frame
bpy.context.scene.frame_step = 10

bpy.context.scene.render.resolution_x = 240
bpy.context.scene.render.resolution_y = 240

# render transparent background
bpy.context.scene.render.film_transparent = True

# degree y z by index
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

for i, roll in enumerate(rolls):
    reset_rotation_values()
    animate_roll(roll[0], roll_count, roll[1], roll[2])
    
    # generate images from animation
    path = PARENT_PATH + str(i + 1) + "\\"
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(animation=True, write_still=True)
