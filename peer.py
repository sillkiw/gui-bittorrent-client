import socket
import logging
class Peer:
    def __init__(pr,ip,port):
        pr.ip = ip
        pr.port = port
        pr.socket = socket.socket()
        pr.live =False
    def connect(pr):
        try:
            pr.socket = socket.create_connection((pr.ip,pr.port),timeout=2)
            pr.socket.setblocking(False)
            pr.live = True
        except Exception as e:
            logging.info(f"NO CONNECTION {pr.ip}")
            return False
        return  True
    def sent_message(pr,msg):
        try:
            pr.socket.send(msg)
        except Exception as e:
            pr.healthy = False
            logging.error("Failed to send to peer : %s" % e.__str__())