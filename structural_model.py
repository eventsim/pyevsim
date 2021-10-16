from definition import CoreModel, ModelType
from collections import OrderedDict

class StructuralModel(CoreModel):
    def __init__(self, _name=""):
        super(StructuralModel, self).__init__(_name, ModelType.STRUCTURAL)

        self._models = []

        self.external_input_coupling_map = {}
        self.external_output_coupling_map = {}
        self.internal_coupling_map = {}

    def insert_model(self, model):
        self._models.append(model)

    def retrieve_models(self):
        return self._models

    def insert_external_input_coupling(self, src_port, internal_model, dst_port):
        if (self, src_port) not in self.external_input_coupling_map:
            self.external_input_coupling_map[(self, src_port)] = [(internal_model, dst_port)]
        else:
            self.external_input_coupling_map[(self, src_port)].append((internal_model, dst_port))

    def insert_external_output_coupling(self, internal_model, src_port, dst_port):
        self.external_output_coupling_map[(internal_model, src_port)] = (self, dst_port)
        pass

    def insert_internal_coupling(self, src_model, src_port, dst_model, dst_port):
        if (src_model, src_port) not in self.internal_coupling_map:
            self.internal_coupling_map[(src_model, src_port)] = [(dst_model, dst_port)]
        else:
            self.internal_coupling_map[(src_model, src_port)].append((dst_model, dst_port))
        pass

    def retrieve_external_input_coupling(self):
        return self.external_input_coupling_map

    def retrieve_external_output_coupling(self):
        return self.external_output_coupling_map

    def retrieve_internal_coupling(self):
        return self.internal_coupling_map

    def get_create_time(self):
        return 0
'''
TODO: serialize using dill
    def serialize(self):
        json_obj = OrderedDict()
        json_obj["name"] = self._name
        json_obj["models"] = self._models
        json_obj["input_ports"] = self.retrieve_input_ports()
        json_obj["output_ports"] = self.retrieve_output_ports()
        json_obj["external_trans"] = self.external_transition_map_state
        json_obj["internal_trans"] = self.internal_transition_map_state
        return json_obj

    def deserialize(self, json):
        self._name = json["name"]
        for k, v in json["states"].items():
            self.insert_state(k, v)

        # Handle In ports
        for port in json["input_ports"]:
            self.insert_input_port(port)

        # Handle out ports
        for port in json["output_ports"]:
            self.insert_output_port(port)

        # Handle External Transition
        for k, v in json["external_trans"].items():
            for ns in v:
                self.insert_external_transition(k, ns[0], ns[1])

        # Handle Internal Transition
        for k, v in json["internal_trans"].items():
            for ns in v:
                self.insert_internal_transition(k, ns[0], ns[1])
'''