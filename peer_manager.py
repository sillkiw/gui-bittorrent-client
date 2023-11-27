import logging
class PeerManager:
    def __init__(pmg,tracker):
        pmg.tracker = tracker
        peers = []
    def add_peers(pmg):
        for peer in pmg.tracker.connected_peers:
            if pmg.handshake(peer):
                pmg.peers.append(peer)
            else:
                logging.error(f"Can't handshake with {peer.id}")
    def handshake(pmg,peer):
        try:
            handshake_message = pmg.tracker.HANDSHAKE
            peer.sent_message(handshake_message)
            logging.info(f"new peer {peer.ip}")
            return True
        except Exception as e:
            logging.error(f"Handshake error with {peer.ip}")