from SocketServer import ThreadingTCPServer as _ThreadingTCPServer

class ThreadingTCPServer(_ThreadingTCPServer):

    allow_reuse_address = True
