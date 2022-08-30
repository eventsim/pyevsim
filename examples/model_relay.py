from pyevsim import SystemSimulator, BehaviorModelExecutor, SysMessage
from pyevsim.definition import *
import datetime

class PEG(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)

        self.insert_input_port("start")
        self.insert_output_port("process")

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "Generate"

    def output(self):
        msg = SysMessage(self.get_name(), "process")
        msg.insert(f"[Gen][OUT]: {datetime.datetime.now()}")
        return msg
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

class MsgRecv (BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_input_port("recv")

    def ext_trans(self,port, msg):
        if port == "recv":
            print(f"[MsgRecv][IN]: {datetime.datetime.now()}")
            data = msg.retrieve()
            print(data[0])
            self._cur_state = "Wait"

    def output(self):
        return None
        
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"

# System Simulator Initialization
ss = SystemSimulator()
ss.register_engine("first", "REAL_TIME", 1)
ss.get_engine("first").insert_input_port("start")
gen = PEG(0, Infinite, "Gen", "first")
ss.get_engine("first").register_entity(gen)
proc = MsgRecv(0, Infinite, "Proc", "first")
ss.get_engine("first").register_entity(proc)
ss.get_engine("first").coupling_relation(None, "start", gen, "start")
ss.get_engine("first").coupling_relation(gen, "process", proc, "recv")
ss.get_engine("first").insert_external_event("start", None)
ss.get_engine("first").simulate()
