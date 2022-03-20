from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime

#from sshkeyboard import listen_keyboard

class Keyboard(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("WAIT")
        self.insert_state("WAIT", Infinite)

        self.insert_input_port("key")

    def ext_trans(self, port, msg):
        if port == "key":
            data = msg.retrieve()
            print(data[0])
        pass

    def output(self):
        return None
        
    def int_trans(self):
        pass

class Generator(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("start")
        self.insert_output_port("process")
        self.msg_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "MOVE"

    def output(self):
        msg = SysMessage(self.get_name(), "process")
        print(f"[Gen][OUT]: {datetime.datetime.now()}")
        msg.insert(self.msg_list.pop(0))
        return msg
        
    def int_trans(self):
        if self._cur_state == "MOVE" and not self.msg_list:
            self._cur_state = "IDLE"
        else:
            self._cur_state = "MOVE"

class Processor(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 2)

        self.insert_input_port("process")

        self.msg_list = []

    def ext_trans(self,port, msg):
        if port == "process":
            print(f"[Proc][IN]: {datetime.datetime.now()}")
            self.cancel_rescheduling()
            data = msg.retrieve()
            self.msg_list.append(data[0])
            self._cur_state = "PROCESS"

    def output(self):
        print(f"[Proc][OUT]: {datetime.datetime.now()}")
        print("|".join(map(str, self.msg_list)))
        return None
        

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"

# System Simulator Initialization
se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 0.5)

k = Keyboard(0, Infinite, "key", "sname")
se.get_engine("sname").insert_input_port("key")
se.get_engine("sname").register_entity(k)
se.get_engine("sname").coupling_relation(None, "key", k, "key")

se.register_engine("sname2", "REAL_TIME", 0.5)
se.get_engine("sname2").insert_input_port("start")

gen = Generator(0, Infinite, "Gen", "sname")
se.get_engine("sname2").register_entity(gen)

proc = Processor(0, Infinite, "Proc", "sname")
se.get_engine("sname2").register_entity(proc)

se.get_engine("sname2").coupling_relation(None, "start", gen, "start")
se.get_engine("sname2").coupling_relation(gen, "process", proc, "process")

#se.get_engine("sname").simulate()
print("DD")
se.exec_non_block_simulate(["sname", "sname2"])
se.get_engine("sname2").insert_external_event("start", None)

'''
def key_press(key):
    print(f"'{key}' pressed")
    se.get_engine("sname").insert_external_event("key", key)

listen_keyboard(on_press=key_press)
'''