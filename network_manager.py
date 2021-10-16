from definition import SingletonType

class NetworkManager(object):
	__metaclass__ = SingletonType
	_network_library = None
	# TODO: Implement Receive Handler
	#_receive_handler = None

	@staticmethod
	def register_network_library(netlib):
		NetworkManager._network_library = netlib
		pass

	@staticmethod
	def run_nonblocking_mode():
		pass

	@staticmethod
	def run_blocking_mode():
		pass

	@staticmethod
	def udp_send_string(host, port, contents):
		#byte_contents = contents.encode()
		byte_contents = contents
		NetworkManager._network_library.set_active(0)
		NetworkManager._network_library.set_remote_host(host)
		NetworkManager._network_library.set_remote_port(port)
		NetworkManager._network_library.set_active(1)
		
		NetworkManager._network_library.send(byte_contents)

	@staticmethod
	def register_receive_handler(handler):
		#_receive_handler = handler
		pass

	@staticmethod
	def connect(host, port):
		NetworkManager._network_library.connect(host, port)

	@staticmethod
	def tcp_send_string(contents):
		byte_contents = contents.encode()
		NetworkManager._network_library.send(byte_contents)