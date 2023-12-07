from struct import pack,unpack


#HandShake <pstrlen><pstr><reserved><info_hash><peer_id>
HS_PSTR = b"BitTorrent protocol"
HS_PSTRLEN = len(HS_PSTR)
def handshake_msg_to_bytes(peer_id,info_hash):
    reserved = b'\x00' * 8
    return pack(">B{}s8s20s20s".format(HS_PSTRLEN),
                         HS_PSTRLEN,
                         HS_PSTR,
                         reserved,
                         info_hash,
                         peer_id)

#KeepAlive keep-alive: <len=0000> нет message ID  нет payload
KEEP_ALIVE_TOTAL_LENGTH = 4
KEEP_ALIVE_PAYLOAD_LENGTH = 0
def keep_alive_msg_from_bytes(payload):
    payload_length = unpack(">I",payload[:KEEP_ALIVE_TOTAL_LENGTH])
    if payload_length != KEEP_ALIVE_PAYLOAD_LENGTH:
        return Exception("Принятое сообщение не \"KeepAlive\"" )
    return KEEP_ALIVE_TOTAL_LENGTH