from messages import impl_handshake_msg
class PeerManager:
    def __init__(pmg,tracker):
        pmg.tracker = tracker
        pmg.peers = []
        pmg.handshake_message = impl_handshake_msg(pmg.tracker.peer_id,pmg.tracker.info_hash)
    def add_peers(pmg):
        for peer in pmg.tracker.connected_peers:
            if pmg.handshake(peer):
                pmg.peers.append(peer)
            else: 
                print(f"Can't handshake with {peer.ip}")
    def handshake(pmg,peer):
        try:
            peer.sent_message(pmg.handshake_message)
            print(f"HandShake with {peer.ip}")
            return True
        except Exception as e:
            print(f"Handshake error with {peer.ip}")