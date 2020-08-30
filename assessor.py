from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

import os
import subprocess as sp

class Assessor(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("assess")
        self.insert_output_port("done")


    def ext_trans(self,port, msg):
        data = msg.retrieve()
        #print("Assessor")
        #print(str(datetime.datetime.now()) +  " " + str(data[0]))
        #temp = "[%f] %s" % (SystemSimulator().get_engine(self.engine_name).get_global_time(), str(data[0]))
        #print(temp)

    def output(self):
        #temp = "[%f] %s" % (SystemSimulator().get_engine(self.engine_name).get_global_time(), "Human Receiver Object: Move")
        #print(temp)
        return None

    def int_trans(self):
        self._cur_state = "MOVE"