import pybullet as p
cin = p.connect(p.SHARED_MEMORY)
if (cin < 0):
    cin = p.connect(p.GUI)
objects = [p.loadURDF("plane_transparent.urdf", 0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,1.000000)]
objects = [p.loadURDF("microtaur.urdf", 0.039976,0.009323,0.229092,-0.008942,0.004335,0.002684,0.999947)]
ob = objects[0]
jointPositions=[ 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.559188, 0.000000, -0.727137, -1.449781, -1.389430, 0.000000, -0.757030, -1.353416, 0.000000, 0.000000, 0.000000, 0.000000, 1.517423, 0.000000, -0.771448, -1.479265, 1.432109, 0.000000, -0.800399, -1.516784 ]
for jointIndex in range (p.getNumJoints(ob)):
	p.resetJointState(ob,jointIndex,jointPositions[jointIndex])

p.setGravity(0.000000,0.000000,-10.000000)
p.stepSimulation()
p.disconnect()
