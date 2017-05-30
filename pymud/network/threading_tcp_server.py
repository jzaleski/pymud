from six.moves.socketserver import ThreadingTCPServer as ThreadingTCPServer_


class ThreadingTCPServer(ThreadingTCPServer_):
    allow_reuse_address = True
