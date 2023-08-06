import pybullet as p
import odrive
import math
import pybullet_data as pd
odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))

p.connect(p.GUI)
p.setAdditionalSearchPath(pd.getDataPath())
u8 = p.loadURDF("tmotor-u8.urdf")
cpr = odrv0.axis0.encoder.config.cpr
print("cpr=",cpr)

while (1):
  pos = 2.*math.pi*odrv0.axis0.encoder.pos_estimate / float(cpr)
  p.resetJointState(u8,0,pos)

