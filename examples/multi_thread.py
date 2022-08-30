from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime

class PEx(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)

        self.insert_input_port("start")

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"[{self.get_name()}][IN]: {datetime.datetime.now()}")
            self._cur_state = "Generate"

    def output(self):
        print(f"[{self.get_name()}][OUT]: {datetime.datetime.now()}")
        return None
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"


ss = SystemSimulator()

# First Engine
ss.register_engine("first", "REAL_TIME", 1)
ss.get_engine("first").insert_input_port("start")
gen = PEx(0, Infinite, "FGen", "first")
ss.get_engine("first").register_entity(gen)
ss.get_engine("first").coupling_relation(None, "start", gen, "start")
ss.get_engine("first").insert_external_event("start", None)

# Second Engine
ss.register_engine("second", "REAL_TIME", 1)
ss.get_engine("second").insert_input_port("start")
gen = PEx(0, Infinite, "SGen", "second")
ss.get_engine("second").register_entity(gen)
ss.get_engine("second").coupling_relation(None, "start", gen, "start")
ss.get_engine("second").insert_external_event("start", None)

ss.exec_non_block_simulate(["first", "second"])
ss.block()