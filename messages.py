from struct import pack


#HandShake
HS_PSTR = b"BitTorrent protocol"
HS_PSTRLEN = len(HS_PSTR)
def impl_handshake_msg(peer_id,info_hash):
    reserved = b'\x00' * 8
    return pack(">B{}s8s20s20s".format(HS_PSTRLEN),
                         HS_PSTRLEN,
                         HS_PSTR,
                         reserved,
                         info_hash,
                         peer_id)


