import socket
import uuid
import threading

class Node(threading.Thread):
    def __init__(self, host, port, id=None, callback=None, max_connections=10):
        super(Node, self).init()

        self.host = host
        self.port = port
        self.id = id
        self.max_connections = max_connections

        self.end_flag = threading.Event()
        
        self.nodes_inbound = set()
        self.nodes_outbound = set()
        self.nodes_reconnecting = []

        if not id:
            id = str(uuid.uuid4())
        else:
            id = str(id)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_server()

        self.messages_count = {
            "sent": 0,
            "recv": 0,
            "rerr": 0
        }
        
        self.callback = callback
        callback.__call__(host, port, id, max_connections)
    
    @property
    def all_messages(self):
        return sum(self.messages_count.values())
    
    @property
    def all_nodes(self):
        return self.nodes_inbound | self.nodes_outbound
    
    def init_server(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10.0)
        self.sock.listen(1)