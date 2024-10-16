import socket
import uuid
import threading
from datetime import datetime

class Node(threading.Thread):
    def __init__(self, host, port, id=None, callback=None, max_connections=10):
        super(Node, self).init()

        self.host = host
        self.port = port
        self.id = id
        self.max_connections = max_connections

        self.end_flag = threading.Event()
        
        self.nodes_inbound = set() # client connected hosts
        self.nodes_outbound = set() # hosts connected to client

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
    
    @property
    def all_messages(self):
        return sum(self.messages_count.values())
    
    @property
    def all_nodes(self):
        return self.nodes_inbound | self.nodes_outbound
    
    def log(self, message):
        print("%s: %s" % (datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                          message)) # todo: do a proper logging
    
    def init_server(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
    
    def run(self): # server-side of p2p
        self.log("listening on %s:%d" % (self.host, self.port))
        conn, addr = self.sock.accept()
        self.handle_connection(conn, addr)
        with conn:
            while not self.end_flag.is_set():
                try:
                    data = conn.recv(1024)
                    if not data:
                        continue
                    self.handle_outbound_data(data, conn, addr)
                except Exception as e:
                    print(e) # todo: do a proper error handling
                
    def handle_connection(self, conn, addr):
        self.nodes_inbound.add(addr)

    def handle_outbound_data(self, data, conn, addr):
        pass