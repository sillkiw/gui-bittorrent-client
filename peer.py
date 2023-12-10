import socket
from struct import pack,unpack
from messages import LEN,handshake_msg_from_bytes,determinator_of_messages

class Peer:
    def __init__(pr,ip,port):
        pr.ip = ip
        pr.port = port
        pr.answer_from_me = b''
        pr.was_handshake = False
        pr.socket = None
        pr.live =False
    
    def connect(pr):
        try:
            pr.socket = socket.create_connection((pr.ip,pr.port),timeout=0.3)
            pr.socket.setblocking(False)
            pr.live = True
        except Exception as e:
            print(f"NO CONNECTION {pr.ip}")
            return False
        return  True
    
    def sent_message(pr,msg):
        try:
            pr.socket.send(msg)
        except Exception as e:
            pr.live = False
            print("Failed to send to peer : %s" % e.__str__())
    
    def unpack_handshake(pr):
        try:
            shift_to_another_message = handshake_msg_from_bytes(pr)
            pr.was_handshake = True
            pr.answer_from_me = pr.answer_from_me[shift_to_another_message:]
            print(f"Получено ответное сообщение \"HandShake\" от {pr.ip}")
            return True
        except Exception as e:
            print(f"Пир {pr.ip} не отправил ответный Handshake message/ или допустил в нем ошибку")
            pr.live = False
        return False




    def unpack_messages(pr):
        while len(pr.answer_from_me) > LEN and pr.live:
            if pr.was_handshake:
                pr.unpack_handshake()
                continue
            #Получение первой части каждого сообщения <len>
            message_len_, = unpack(">U",pr.answer_from_me[:LEN])
            #Общий размер сообщения указаннный в <len> + 4 байта от самого <len>
            total_length = message_len_ + LEN

            if len(pr.answer_from_me) < total_length:
                #Заявленный размер не соответсвует реальному размеру сообщению
                break
            else:
                undetermine_message = pr.answer_from_me[:total_length]
                pr.answer_from_me = pr.answer_from_me[total_length:]

            try:
                parts_of_message = determinator_of_messages(undetermine_message)
            