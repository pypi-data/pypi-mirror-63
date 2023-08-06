import pybullet as p
import pybullet_data as pd
import time

p.connect(p.GUI)
p.setAdditionalSearchPath(pd.getDataPath())
flags = 0
flags += p.URDF_MAINTAIN_LINK_ORDER
flags += p.URDF_MERGE_FIXED_LINKS
flags += p.URDF_IGNORE_VISUAL_SHAPES
flags += p.URDF_ENABLE_CACHED_GRAPHICS_SHAPES
flags += p.URDF_PRINT_URDF_INFO
p.loadURDF("plane.urdf")

start_pos = [0,0,1]
pet = p.loadURDF("alphapet/models/v0/alphapet.urdf",start_pos, flags=flags)
print("pet #joints = ", p.getNumJoints(pet))
for j in range (p.getNumJoints(pet)):
  p.setJointMotorControl2(pet,j,p.POSITION_CONTROL, force=200)

gravZid = p.addUserDebugParameter("gravityZ", -10,10,0)
p.setGravity(0,0,-9.81)
dt = 1./240.
p.setTimeStep(dt)

while p.isConnected():
   gravZ = p.readUserDebugParameter(gravZid)
   p.setGravity(0,0,gravZ)
   p.stepSimulation()
   time.sleep(dt)



