from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime

import dill
import zmq
from io import BytesIO
import threading

context = zmq.Context()

#  Socket to talk to server
print("ZMQ PUB Mode: Binding Port 5555")
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

class Generator(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("MOVE", 1)

        self.insert_input_port("start")
        self.insert_output_port("process")
        self.my_var = 0;

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"[Gen][IN]: {datetime.datetime.now()}")
            self._cur_state = "MOVE"

    def output(self):
        msg = SysMessage(self.get_name(), "process")
        print(f"[Gen][{self.my_var}]: {datetime.datetime.now()}")
        return msg
        
    def int_trans(self):
        if self._cur_state == "MOVE":
            self.my_var += 1
            self._cur_state = "MOVE"
        else:
            self._cur_state = "IDLE"

    def is_migrate(self):
       if self.my_var % 5 == 4:
            self.my_var = 0
            return True
       else:
            return False

# System Simulator Initialization
se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 0.01)

se.register_engine("sname2", "REAL_TIME", 0.01)
se.get_engine("sname2").insert_input_port("start")

gen = Generator(0, Infinite, "Gen", "sname")
se.get_engine("sname2").register_entity(gen)

se.get_engine("sname2").coupling_relation(None, "start", gen, "start")

se.get_engine("sname2").insert_external_event("start", None)

socket2 = context.socket(zmq.SUB)
socket2.setsockopt(zmq.SUBSCRIBE, b"")
socket2.connect ("tcp://localhost:5556" )

def recv_thread():
    while True:
        msg = socket2.recv()
        print(f"model receved")
        model = dill.temp.loadIO(BytesIO(msg))

        se.get_engine("sname2").register_entity(model)
 
t = threading.Thread(target=recv_thread, args=())
t.start()

while True:
    se.get_engine("sname2").simulate(1)

    migrate_models = se.get_engine("sname2").get_entity("Gen")
    for model in migrate_models:
        if model.is_migrate():
            #print(se.get_engine("sname2").get_entity("Gen"))
            dump = dill.temp.dumpIO(model)
            dump.seek(0)
            socket.send(dump.read())
            se.get_engine("sname2").remove_entity("Gen")
