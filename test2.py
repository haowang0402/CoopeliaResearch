from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.arms.panda import Panda
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
from pyrep.errors import ConfigurationPathError
from pyrep.objects.dummy import Dummy
import numpy as np
import math
def move_arm(arm,position,quaternion, ignore_collisions=False):
    arm_path = arm.get_path(position,
                            quaternion=quaternion,
                            ignore_collisions=ignore_collisions)
    arm_path.visualize()
    done = False
    while not done:
        done = arm_path.step()
        pr.step()
    arm_path.clear_visualization()

SCENE_FILE = join(dirname(abspath(__file__)), 'double_panda.ttt')
pr = PyRep()
pr.launch(SCENE_FILE, headless=False)
pr.start()
panda = Panda()
cubes = []
pos = [[0.675, -0.45, 0.82],[0.65, -0.225, 0.82],[0.45, -0.175, 0.82],[0.425, 0.2, 0.82],[0.625, 0.275, 0.82],[0.625, 0.525, 0.82]]
dummies = [Dummy.create() for i in range(0,6)]
for i in range(0,6):
    cube = Shape.create(type = PrimitiveShape.CUBOID, size = [0.1,0.1,0.1], color = [1.0,0.1,0.1])
    cubes.append(cube)
    cube.set_position(pos[i])
    dummies[i].set_position(pos[i])
for i in range(0,3):
    path = panda.get_path(
            position=pos, euler=[0, math.radians(180), 0])
    except ConfigurationPathError as e:
        print('Could not find path')
        continue
    move_arm(panda1,pos[2*i+1],dummies[2*i+1].get_quaternion())
pr.step()
pr.stop()
pr.shutdown()
