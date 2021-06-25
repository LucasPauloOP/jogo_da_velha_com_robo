import sim

class Arm_controller(object):
    def __init__(self):
        self.clientID = None
        self.joint_handles = []
        self.step = self.deg_to_rad(40)
        self.last_pos = []
        return

    def set_up_connection(self):
       # print("Starter")
        sim.simxFinish(-1) # just in case, close all opened connections
        self.clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5) # start a connection

        if self.clientID!=-1:
            #print("Connected to remote API server")
            self.set_up_joints_handles()
        else:
            #print("Not connected to remote API server")
            sys.exit("Could not connect")
        return


    def terminate_connection(self):
        sim.simxStopSimulation(self.clientID, sim.simx_opmode_oneshot)
        return

    def set_up_joints_handles(self):

        err_code1, joint_handle1 = sim.simxGetObjectHandle(
                                        self.clientID,
                                        "uarm_motor1",
                                        sim.simx_opmode_blocking)
        err_code2, joint_handle2 = sim.simxGetObjectHandle(
                                        self.clientID,
                                        "uarm_motor2",
                                        sim.simx_opmode_blocking)
        err_code3, joint_handle3 = sim.simxGetObjectHandle(
                                        self.clientID,
                                        "uarm_motor3",
                                        sim.simx_opmode_blocking)
        err_code4, joint_handle4 = sim.simxGetObjectHandle(
                                        self.clientID,
                                        "uarm_motor4",
                                        sim.simx_opmode_blocking)
      #  err_code5, joint_handle5 = sim.simxGetObjectHandle(
      #                                  self.clientID,
      #                                  "UR3_joint5",
      #                                  sim.simx_opmode_blocking)
      #  err_code6, joint_handle6 = sim.simxGetObjectHandle(
      #                                  self.clientID,
      #                                  "UR3_joint6",
      #                                  sim.simx_opmode_blocking)
        self.joint_handles = [joint_handle1,
                              joint_handle2,
                              joint_handle3,
                              joint_handle4]
                             # joint_handle5,
                             # joint_handle6]
        for i in range(4):
            err_code, last_pos = sim.simxGetJointPosition(
                                    self.clientID,
                                    self.joint_handles[i],
                                    sim.simx_opmode_streaming)
            self.last_pos.append(last_pos)
        return

    def deg_to_rad(self, deg):
        rad = (deg*3.14)/180
        return rad

    def increase_joint_deg(self, joint_num):
        #print(joint_num)

        sim.simxPauseCommunication(self.clientID, True)
        err_code = sim.simxSetJointTargetPosition(
                    self.clientID,
                    self.joint_handles[joint_num],
                    self.deg_to_rad(self.last_pos[joint_num]+self.step),
                    sim.simx_opmode_streaming)
        sim.simxPauseCommunication(self.clientID, False)

        self.last_pos[joint_num] += 5 + self.step
        if self.last_pos[joint_num] > 180:
            self.last_pos[joint_num] = 0
        elif self.last_pos[joint_num] < 0:
            self.last_pos[joint_num] = 0
        #print("Motor: ", joint_num)
        #print(self.last_pos[joint_num])


    def decrease_joint_deg(self, joint_num):
        sim.simxPauseCommunication(self.clientID, True)
        err_code = sim.simxSetJointTargetPosition(
                        self.clientID,
                        self.joint_handles[joint_num],
                        self.deg_to_rad(self.last_pos[joint_num]-self.step),
                        sim.simx_opmode_streaming)
        sim.simxPauseCommunication(self.clientID, False)
        self.last_pos[joint_num] -= self.step + 5
        if self.last_pos[joint_num] > 180:
            self.last_pos[joint_num] = 0
        elif self.last_pos[joint_num] < 0:
            self.last_pos[joint_num] = 0
        #print("Motor ", joint_num)
        #print(self.last_pos[joint_num])

    # open rg2
    def openRG2(self):
        rgName = 'RG2'
        clientID = self.clientID
        res, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(clientID, rgName, \
                                                                                    sim.sim_scripttype_childscript,
                                                                                    'rg2Open', [], [], [], b'',
                                                                                    sim.simx_opmode_blocking)

    # close rg2
    def closeRG2(self):
        rgName = 'RG2'
        clientID = self.clientID
        res, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(clientID, rgName, \
                                                                                    sim.sim_scripttype_childscript,
                                                                                    'rg2Close', [], [], [], b'',
                                                                                    sim.simx_opmode_blocking)