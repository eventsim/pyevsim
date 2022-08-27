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
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "Generate"

    def output(self):
        print(f"[Gen][OUT]: {datetime.datetime.now()}")
        return None
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"


ss = SystemSimulator()

ss.register_engine("simple", "REAL_TIME", 1)
ss.get_engine("simple").insert_input_port("start")
gen = PEx(0, Infinite, "Gen", "simple")
ss.get_engine("simple").register_entity(gen)

ss.get_engine("simple").coupling_relation(None, "start", gen, "start")

ss.get_engine("simple").insert_external_event("start", None)
ss.get_engine("simple").simulate()

