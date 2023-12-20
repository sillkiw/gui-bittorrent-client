import socket,messages
from struct import pack,unpack
from bitstring import BitArray
import time

class Peer:
    def __init__(pr,ip,port,tracker):
        pr.ip = ip
        pr.port = port
        pr.tracker = tracker
        pr.answer_from_me = b''
        pr.was_handshake = False
        pr.socket = None
        pr.alive =False
        pr.last_call = 0.0
        pr.fill_factor = []
        pr.show = True
        pr.activity_factor = 0
        pr.bitfield = BitArray(pr.tracker.torrent.number_of_pieces)
        #Начальные значения состояний подключения по спецификации таие
        pr.state = {
            'am_choking' : True,
            'am_interested' : False,
            'peer_choking' : True,
            'peer_interested' : False,

        }
    def connect(pr):
        try:
            pr.socket = socket.create_connection((pr.ip,pr.port),timeout=0.3)
            pr.socket.settimeout(0.05)
            pr.alive = True
        except Exception as e:
            return False
        return  True
    
    def is_open(pr):
        now = time.time()
        return (now - pr.last_call) > 0.3

    def am_interested(pr):
        return pr.state['am_interested']
    
    def am_choking(pr):
        return pr.state['am_choking']

    def is_choking(pr):
        return pr.state['peer_choking']

    def is_unchoked(pr):
        return not pr.is_choking()

    def sent_message(pr,msg):
        try:
            pr.socket.send(msg)
            pr.last_call = time.time()
        except Exception as e:
            pr.activity_factor = 0
            
    
    def handle_handshake(pr):
        try:
            shift_to_another_message = messages.handshake_msg_from_bytes(pr.answer_from_me,pr.tracker.info_hash)
            pr.was_handshake = True
            pr.answer_from_me = pr.answer_from_me[shift_to_another_message:]
            print(f"Получено ответное сообщение \"HandShake\" от {pr.ip}")
            return True
        except Exception as e:
            print(f"Пир {pr.ip} не отправил ответный Handshake message/ или допустил в нем ошибку")
            pr.alive = False
        return False
    
    def handle_keep_alive(pr):
        try:
            shift_to_another_message = messages.keep_alive_msg_from_bytes(pr.answer_from_me)
            pr.answer_from_me = pr.answer_from_me[shift_to_another_message:]   
            print("Получение keepalive message")
            return True
        except Exception as e:
            pass
        return False
    
    def handle_choke(pr):
        print(f"Получение сообщения Choke от {pr.ip}")
        pr.state['peer_choking'] = True
    
    def handle_unchoke(pr):
        print(f"Получение сообщения Unchoke от {pr.ip}")
        pr.state['peer_choking'] = False
    
    def handle_interested(pr):
        print(f"Получение сообщения Interested от {pr.ip}")
        pr.state['peer_interested'] = True
        
        if pr.am_choking():
            unchoke = messages.unchoke_msg_to_bytes()
            pr.sent_message(unchoke)

    def handle_not_interested(pr):
        print(f"Получение сообщения Not Interested от {pr.ip}")
        pr.state['peer_interested'] = False

    def handle_have(pr,message_have):
        print(f"Получение сообщения Have от {pr.ip}")
        pr.bitfield[message_have['piece_index']] = True

        if pr.is_choking() and not pr.am_interested():
            interested = messages.interested_msg_to_bytes()
            print(f"Отправка сообщения Interested к {pr.ip}")
            pr.sent_message(interested)
            pr.state['am_interested'] = True
      

    def handle_bitfield(pr,message_bitfield):
        print(f"Получение сообщения Bitfield от {pr.ip}")
        pr.bitfield = message_bitfield['bitfield']
        
        if pr.is_choking() and not pr.am_interested():
            interested = messages.interested_msg_to_bytes()
            print(f"Отправка сообщения Interested к {pr.ip}")
            pr.sent_message(interested)
            pr.state['am_interested'] = True
    
    def has_piece(pr,index):
        return pr.bitfield[index]

    def handle_request(pr,request):
        print(f"Получение сообщения Request от {pr.ip}")
    
    def handle_cancel(pr,request):
        print(f"Получение сообщения Cancel от {pr.ip}")
    
    def handle_port(pr):
        print(f"Получение сообщения Port от {pr.ip}")
    
    def unpack_messages(pr):
        while len(pr.answer_from_me) > messages.LEN and pr.alive:
            if not(pr.was_handshake):
                pr.handle_handshake()
                continue
            if pr.handle_keep_alive():
                continue
            #Получение первой части каждого сообщения <len>
            message_len_, = unpack(">I",pr.answer_from_me[:messages.LEN])
            #Общий размер сообщения указаннный в <len> + 4 байта от самого <len>
            total_length = message_len_ + messages.LEN

            if len(pr.answer_from_me) < total_length:
                #Заявленный размер не соответсвует реальному размеру сообщения
                break
            else:
                undetermine_message = pr.answer_from_me[:total_length]
                pr.answer_from_me = pr.answer_from_me[total_length:]

            try:
                recv_message = messages.determinator_of_messages(undetermine_message)
                if recv_message:
                    yield recv_message
            except Exception as e:
                print(e.__str__)
    
    def __hash__(pr):
        return "%s:%d" % (pr.ip, pr.port)