from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.arms.panda import Panda
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
from pyrep.errors import ConfigurationPathError
import numpy as np
import math

LOOPS = 10
SCENE_FILE = join(dirname(abspath(__file__)), 'double_panda.ttt')
pr = PyRep()
pr.launch(SCENE_FILE, headless=False)
pr.start()
agent = Panda(0)
agent2 = Panda(1)
# We could have made this target in the scene, but lets create one dynamically
target = Shape.create(type=PrimitiveShape.SPHERE,
                      size=[0.05, 0.05, 0.05],
                      color=[1.0, 0.1, 0.1],
                      static=True, respondable=False)

target2 = Shape.create(type = PrimitiveShape.SPHERE, size = [0.05,0.05,0.05], color = [0.0,1.0,0.0],position=[0.5,0.1,1])

position_min, position_max = [0.8, -0.2, 1.0], [1.0, 0.2, 1.4]

starting_joint_positions = agent.get_joint_positions()

starting_joint_positions2 = agent2.get_joint_positions()
for i in range(LOOPS):

    agent.set_joint_positions(starting_joint_positions)
    agent2.set_joint_positions(starting_joint_positions2)
    pos = list(np.random.uniform(position_min, position_max))
    target.set_position(pos)
    target2.set_position([0.5,0.1,1])
    try:
        path = agent.get_path(
            position=pos, euler= [0, math.radians(180), 0])
    except ConfigurationPathError as e:
        print('Could not find path with Panda')
        continue

    try:
        path2 = agent2.get_path(
            position=[0.5,0.1,1], euler= [0, math.radians(180), 0])
    except ConfigurationPathError as e:
        print('Could not find path with Panda#0')
        continue
    # Step the simulation and advance the agent along the path
    done = False
    while not done:
        done = path.step()
    print('Reached target %d by Panda!' % i)

    done2 = False
    while not done2:
        done2 = path2.step()
        pr.step()
    print('Readched target %d by Panda#0'% i )
pr.stop()
pr.shutdown()
