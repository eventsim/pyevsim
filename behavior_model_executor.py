from evsim.system_object import SysObject
from abc import abstractmethod
from evsim.behavior_model import BehaviorModel
from evsim.definition import *

class BehaviorModelExecutor(SysObject, BehaviorModel):
    def __init__(self, instantiate_time=Infinite, destruct_time=Infinite, name=".", engine_name="default"):
        SysObject.__init__(self)
        BehaviorModel.__init__(self, name)
        self.engine_name = engine_name
        self._instance_t = instantiate_time
        self._destruct_t = destruct_time
        self._next_event_t = 0
        self._cur_state = ""
        # self._state_lst = []
        #self._time_map = {}
        # self._in_port_lst = []
        # self._out_port_lst = []
        self.RequestedTime = float("inf")
        self._not_available = None

    def __str__(self):
        return "[N]:{0}, [S]:{1}".format(self.get_name(), self._cur_state)

    def get_engine_name(self):
        return self.engine_name

    def set_engine_name(self, engine_name):
        self.engine_name = engine_name

    def get_create_time(self):
        return self._instance_t

    def get_destruct_time(self):
        return self._destruct_t

    # state management
    def get_cur_state(self):
        return self._cur_state

    def init_state(self, state):
        self._cur_state = state

    # External Transition
    @abstractmethod
    def ext_trans(self, port, msg):
        pass

    # Internal Transition
    @abstractmethod
    def int_trans(self):
        pass

    # Output Function
    @abstractmethod
    def output(self):
        pass

    # Time Advanced Function
    def time_advance(self):
        if self._cur_state in self._states:
            return self._states[self._cur_state]
        else:
            return -1

    def set_req_time(self, global_time):
        if self.time_advance() == Infinite:
            self.RequestedTime = Infinite
        else:
            self.RequestedTime = global_time + self.time_advance()

    def get_req_time(self):
        return self.RequestedTime
