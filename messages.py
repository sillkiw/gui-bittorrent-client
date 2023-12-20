'''Модуль с функциями для работы с сообщениями, определенными в BitTorrent protocol'''
from random import randint
from struct import pack,unpack
from bitstring import BitArray
'''Вспомогательные функции и константы'''

#Каждое сообщение начинается с <len> | размер фиксированный - 4 байта 
LEN = 4

def name_msg_from_bytes_maker(payload,cons_total_length,cons_payload_length,cons_id,message_name):
    payload_length,message_id = unpack(">IB",payload[:cons_total_length])
    if message_id != cons_id or cons_payload_length != payload_length :
        raise Exception(f"Принятое сообщение не \"{message_name}\"")
    return {'len':payload_length,
            "id" :message_id,
            }



'''UPD tracker'''

'''CONNECTION MESSAGES'''
MAGIC_CONSTANT = 0x41727101980
PROTOCOL_ID = pack('>Q',MAGIC_CONSTANT)
CONNECTION_ACTION = 0
CONNECTION_ACTION_PACK = pack('>I',CONNECTION_ACTION)
CONNECTION_MESSAGE_SIZE = 16

def upd_tracker_connection_form_message():
    """
        connect = <connection_id><action><transaction_id>
            - connection_id = 0x41727101980 64-bit integer
            - action = 0 32-bit integer
            - transaction_id = random 32-bit integer

        Total length = 64 + 32 + 32 = 128 bytes
    """
    trans_id = randint(1000,100000)
    return PROTOCOL_ID +  CONNECTION_ACTION_PACK + pack(">I",trans_id),trans_id
   
def upd_tracker_connection_form_message_recieve(payload,made_trans_id):
    """
        connect_response = <action><transaction_id><connection_id>
        - action = 0 32-bit integer
        - transaction_id = с первого запроса 32-bit integer
        - connection_id = 0x41727101980 64-bit integer

        Total length = 64 + 32 + 32 = 128 bytes
    
    """
    if len(payload) < CONNECTION_MESSAGE_SIZE:
        return False,None

    action, = unpack(">I",payload[:4])    
    trans_id, =  unpack(">I",payload[4:8])
    conn_id, = unpack(">Q",payload[8:])

    if action != CONNECTION_ACTION  or trans_id != made_trans_id:
        return False,None
    else:

        return True,conn_id

'''ANNOUNCE MESSAGES'''
ANNOUNCE_ACTION = 1
ANNOUNCE_ACTION_PACK = pack('>I',ANNOUNCE_ACTION)
ANNOUNCE_RESPONSE_MIN_SIZE = 20

#TODO:сделать комменты 
def upd_tracker_annnounce_form_message(peer_id,info_hash,conn_id):
    trans_id = randint(1000,100000)
    trans_id_pack = pack(">I",trans_id)
    downloaded = left = uploaded = pack('>Q',0)
    event = ip = key = pack('>I',0)
    num_want = pack('>i',-1)
    port = pack('>H',8000)
    conn_id_pack = pack(">Q",conn_id)

    return (conn_id_pack + ANNOUNCE_ACTION_PACK + trans_id_pack + info_hash + peer_id + downloaded + left + uploaded + event + ip + key + num_want + port),trans_id

def upd_tracker_annnounce_form_message_recieve(payload,given_trans_id):

    if len(payload) < ANNOUNCE_RESPONSE_MIN_SIZE:
        return False,None
    
    action, = unpack('>I', payload[:4])
    transaction_id, = unpack('>I', payload[4:8])
    interval, = unpack('>I', payload[8:12])
    leechers, = unpack('>I', payload[12:16])
    seeders, = unpack('>I', payload[16:20])
    peers_data = payload[20:]

    if action != ANNOUNCE_ACTION or transaction_id != given_trans_id:
        return False,None
    else:
        return True,peers_data
    
'''END | UPD tracker'''

'''HandShake'''
HANDSHAKE_PAYLOAD_LENGTH = HANDSHAKE_TOTAL_LENGTH = 68
HS_PSTR = b"BitTorrent protocol"
HS_PSTRLEN = len(HS_PSTR)

def handshake_msg_to_bytes(peer_id,info_hash):
    '''
    -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
        Обязательное сообщение при первом подключении к пиру, после обмена ими устанавливается связь между пирами
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
        pstr      -  имя протокола, значение определено однозначно : BitTorrent protocol
        prstlen   -  длина pstr, значение определено одозначно и равно 19
        reserved  -  8 нулевых байтов, каждый из этих байтов может быть использован для изменения поведения протокола
        info_hash -  info_hash, преобразован из торрента | отправленный в трекер
        peer_id   -  отправленный в трекер
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
        <pstrlen>    =  1 (byte)
        <pstr>       = 19 (byte)
        <reserved    =  8 (byte)
        <info_hash>  = 20 (byte)
        <peer_id>    = 20 (byte)
        ------------------------ +
        payload_length = total_length = 68 (byte)
    -----------------------------------------------------------------------------------------------------------------
    '''
    reserved = b'\x00' * 8
    return pack(f">B{HS_PSTRLEN}s8s20s20s",
                         HS_PSTRLEN,
                         HS_PSTR,
                         reserved,
                         info_hash,
                         peer_id)

def handshake_msg_from_bytes(payload,info_hash):
    pstrlen, = unpack(">B",payload[:1])
    pstr,reserved,info_hash_chk,peer_id = unpack(f">{pstrlen}s8s20s20s",payload[1:HANDSHAKE_TOTAL_LENGTH])
    if pstr != HS_PSTR:
        raise Exception("Ошибка в названии протокола")
    if info_hash != info_hash_chk:
        raise Exception("info_hash пира не совпадает с исходным")
    return HANDSHAKE_PAYLOAD_LENGTH

'''
KeepAlive message:
    -----------------------------------------------------------------------------------------------------------------
    Назначение: 
    -----------------------------------------------------------------------------------------------------------------
        Если спустя некоторого времени пир не получает никаких сообщений от другого пира, он может оборвать соедение. 
        Это сообщение нужно для поддержания соединения в активном состоянии, если в течение заданного периода времени 
        не было отправлено ни одного сообщения.
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        keep-alive: <len=0000>
        len = 0
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
        total_length = <len> = 4(byte)
        payload_length = 0
    -----------------------------------------------------------------------------------------------------------------
'''
KEEP_ALIVE_TOTAL_LENGTH = LEN
KEEP_ALIVE_PAYLOAD_LENGTH = 0

def keep_alive_msg_from_bytes(payload):
    payload_length = unpack(">I",payload[:KEEP_ALIVE_TOTAL_LENGTH])

    if payload_length != KEEP_ALIVE_PAYLOAD_LENGTH:
        raise("Полученное сообщение не Keep-Alive")
    return KEEP_ALIVE_TOTAL_LENGTH

'''
Choke message:
    -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
        Сообщение о том, что пир не будет отправлять части
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        choke: <len=0001><id=0>
        len - фиксированный 
        id  - 0
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
        len = 4 (byte)
        id  = 1 (byte)
        ------------------------ +
        payload_length = 1
        total_length   = 5
    -----------------------------------------------------------------------------------------------------------------
'''
CHOKE_PAYLOAD_LENGTH = 1
CHOKE_TOTAL_LENGTH = LEN + CHOKE_PAYLOAD_LENGTH #5
CHOKE_MESSAGE_ID = 0

def choke_msg_to_bytes():
    return pack(">IB",CHOKE_PAYLOAD_LENGTH,CHOKE_MESSAGE_ID)

def choke_msg_from_bytes(payload):
    return name_msg_from_bytes_maker(payload,
                  CHOKE_TOTAL_LENGTH,
                  CHOKE_PAYLOAD_LENGTH,
                  CHOKE_MESSAGE_ID,
                  "Choke message")

'''
Unchoke message:
    -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
        Сообщение о том, что пир начнет отправлять части
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        choke: <len=0001><id=1>
        len - фиксированный 
        id  - 1
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
        аналогично с Choke
    -----------------------------------------------------------------------------------------------------------------
'''
UNCHOKE_PAYLOAD_LENGTH = 1
UNCHOKE_TOTAL_LENGTH = LEN + UNCHOKE_PAYLOAD_LENGTH
UNCHOKE_MESSAGE_ID = 1

def unchoke_msg_to_bytes():
    return pack(">IB",UNCHOKE_PAYLOAD_LENGTH,UNCHOKE_MESSAGE_ID)

def unchoke_msg_from_bytes(payload):
    return name_msg_from_bytes_maker(payload,
                  UNCHOKE_TOTAL_LENGTH,
                  UNCHOKE_PAYLOAD_LENGTH,
                  UNCHOKE_MESSAGE_ID,
                  "Unchoke message")
'''
Interested message:
    -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
        Сообщение о том, что пир заинтересован в обмене частями
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        <len=0001><id=2>
        len - фиксированный 
        id  - 2
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
        аналогично с Choke
    -----------------------------------------------------------------------------------------------------------------
'''
INTERESTED_PAYLOAD_LENGTH = 1
INTERESTED_TOTAL_LENGTH = LEN + INTERESTED_PAYLOAD_LENGTH
INTERESTED_MESSAGE_ID = 2

def interested_msg_to_bytes():
    return pack(">IB",INTERESTED_PAYLOAD_LENGTH,INTERESTED_MESSAGE_ID)

def interseted_msg_from_bytes(payload):
    return name_msg_from_bytes_maker(payload,
                  INTERESTED_TOTAL_LENGTH,
                  INTERESTED_PAYLOAD_LENGTH,
                  INTERESTED_MESSAGE_ID,
                  "Interested message")

'''
Unterested message:
    -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
        Сообщение о том, что пир незаинтересован в обмене частями
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        <len=0001><id=3>
        len - фиксированный 
        id  - 3
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
        аналогично с Choke
    -----------------------------------------------------------------------------------------------------------------
'''
NOTINTERESTED_PAYLOAD_LENGTH = 1
NOTINTERESTED_TOTAL_LENGTH = LEN + NOTINTERESTED_PAYLOAD_LENGTH
NOTINTERESTED_MESSAGE_ID = 3

def notInterested_msg_from_bytes(payload):
    return name_msg_from_bytes_maker(payload,
                  NOTINTERESTED_TOTAL_LENGTH,
                  NOTINTERESTED_PAYLOAD_LENGTH,
                  NOTINTERESTED_MESSAGE_ID,
                  "Not interested  message")

'''
Have message
   -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
        Сообщение о том, что пир имеет определенную часть
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        have: <len=0005><id=4><piece index>
        len - фиксированный размер сообщения
        id  - 4
        piece index - индекс части, которая есть у пира
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
        len -         4(bytes)
        id  -         1(byte)
        piece_index - 4(bytes)
        ----------------------+
        total_length = 9
        payload_length = 5
    -----------------------------------------------------------------------------------------------------------------

'''
HAVE_PAYLOAD_LEGNTH = 5
HAVE_TOTAL_LENGTH = + LEN + HAVE_PAYLOAD_LEGNTH 
HAVE_MESSAGE_ID = 4

def have_msg_from_bytes(payload):
    payload_length,message_id,piece_index = unpack(">IBI",payload[:HAVE_TOTAL_LENGTH])
    if message_id != HAVE_MESSAGE_ID:
        raise Exception("Это не Have message")
    return {'len':payload_length,
            "id" :message_id,
            "piece_index":piece_index
            }
         
'''
Bitfield message(опцианально)
   -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
        Сообщение отправляется сразу же после Handshake message и служит для того, чтобы сообщить о наличии 
        установленных частей
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        bitfield: <len=0001+X><id=5><bitfield>
        len - нефиксированный размер сообщения
        id  - 5
        bitfield - строка состоящая из 0 и 1 
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
       <len>        = 4 bytes
       <id>         = 1 byte
       <bitfield>   = len(bitfield) (bytes)
       total_length   - ?
       payload_length - ?
    -----------------------------------------------------------------------------------------------------------------

'''
BITFIELD_MESSAGE_ID = 5

def bitfield_msg_from_bytes(payload):
    payload_length,message_id = unpack(">IB",payload[:LEN+1])
    bitfield_length = payload_length - 1

    if message_id != BITFIELD_MESSAGE_ID:
        raise Exception("Не Bitfield message") 
    raw_bitfield, = unpack(f">{bitfield_length}s",payload[5:5+bitfield_length])
    bitfield = BitArray(bytes = raw_bitfield)
    #TODO: Проверить bitfield
    return {'len':payload_length,
            "id" :message_id,
            "bitfield":bitfield,
            }

#TODO: доделать объяснение

'''
Request message
   -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
        Сообщение отправляется сразу же после Handshake message и служит для того, чтобы сообщить о наличии 
        установленных частей
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
        request: <len=0013><id=6><index><begin><length>
        len - фиксированный размер сообщения 13
        id  - 6
        index - число, индекс части
        begin - 
        length
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------
       <len>        = 4 bytes
       <id>         = 1 byte
       <bitfield>   = len(bitfield) (bytes)
       total_length   - ?
       payload_length - ?
    -----------------------------------------------------------------------------------------------------------------

'''
REQUEST_PAYLOAD_LENGTH = 13
REQUEST_TOTAL_LENGTH = LEN + REQUEST_PAYLOAD_LENGTH
REQUEST_MESSAGE_ID = 6

def request_msg_from_bytes(payload):
    payload_length,message_id,index,begin,length = unpack(">IBIII",payload[:REQUEST_TOTAL_LENGTH]) 
    if message_id !=  REQUEST_MESSAGE_ID or payload_length != REQUEST_PAYLOAD_LENGTH:
        raise Exception("Не Request message")
    return {'len':payload_length,
            "id" :message_id,
            "index":index,
            "begin":begin,
            "length":length }

def request_msg_to_bytes(piece_index,block_offset,block_length):
    return pack(">IBIII",REQUEST_PAYLOAD_LENGTH,REQUEST_MESSAGE_ID,piece_index,block_offset,block_length)
#TODO: доделать объяснение

'''
Piece message(опцианально)
   -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
    
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
    
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------

    -----------------------------------------------------------------------------------------------------------------

'''
PIECE_MESSAGE_ID = 7

def piece_msg_from_bytes(payload):
    block_length = len(payload) - (LEN + 9)
    payload_length,message_id,piece_index,begin,block = unpack(f">IBII{block_length}s",payload[:13+block_length])

    if message_id != PIECE_MESSAGE_ID:
         raise Exception("Не Piece message")
    return {'len':payload_length,
            "id" :message_id,
            "piece_index":piece_index,
            "begin":begin,
            "block":block}

'''
 Cancel message(опцианально)
   -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
    
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
    
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------

    -----------------------------------------------------------------------------------------------------------------

'''
CANCEL_PAYLOAD_LENGTH = 13
CANCEL_TOTAL_LENGTH = LEN + CANCEL_PAYLOAD_LENGTH
CANCEL_MESSAGE_ID = 8

def cancel_msg_from_bytes(payload):
    payload_length,message_id,index,begin,length =  unpack(">IBIII", payload[:CANCEL_TOTAL_LENGTH])

    if message_id != CANCEL_MESSAGE_ID:
        raise("Не Cancel message")
    
    return {'len':payload_length,
            "id" :message_id,
            "index":index,
            "begin":begin,
            "length":length }

'''
 Port message(опцианально)
   -----------------------------------------------------------------------------------------------------------------
    Назначение:
    -----------------------------------------------------------------------------------------------------------------
    
    -----------------------------------------------------------------------------------------------------------------
    Вид:
    -----------------------------------------------------------------------------------------------------------------
    
    -----------------------------------------------------------------------------------------------------------------
    Общий размер сообщения и его действительной части:
    -----------------------------------------------------------------------------------------------------------------

    -----------------------------------------------------------------------------------------------------------------

'''
PORT_PAYLOAD_LENGTH = 5
PORT_TOTAL_LENGTH = LEN + PORT_PAYLOAD_LENGTH
PORT_MESSAGE_ID = 9

def port_msg_from_bytes(payload):
    payload_length,message_id,listen_port = unpack(">IBI",payload[:PORT_TOTAL_LENGTH])
    
    if message_id != PORT_MESSAGE_ID:
        raise("Не Port message")
    
    return {'len':payload_length,
            "id" :message_id,
            "listen_port":listen_port,
            }


'''Определитель приходящих сообщений'''
def determinator_of_messages(u_message):
    try:
        u_message_len,u_message_id = unpack(">IB",u_message[:LEN+1]) #размер Len(4 byte) + message_id(1 byte)
    except Exception as e:
        print(F"Возникла ошибка в чтении сообщения {e}")
        return None
    
    map_id_to_message = {
        0 : choke_msg_from_bytes,
        1 : unchoke_msg_from_bytes,
        2 : interseted_msg_from_bytes,
        3 : notInterested_msg_from_bytes,
        4 : have_msg_from_bytes,
        5 : bitfield_msg_from_bytes,
        6 : request_msg_from_bytes,
        7 : piece_msg_from_bytes,
        8 : cancel_msg_from_bytes,
        9 : port_msg_from_bytes
    }
    
    if u_message_id not in (list(map_id_to_message.keys())):
        raise Exception("Ошибка в определении id сообщения")
           
    return map_id_to_message[u_message_id](u_message)


