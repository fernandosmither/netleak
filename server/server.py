from collections import defaultdict
from typing import Dict, List
from signal_protocol import state


class SignalServer:
    def __init__(self):
        self.user_prekey_bundles: Dict[str, List[state.PreKeyBundle]] = {}
        self.message_queue = defaultdict(list)

    def register_user(self, user_id, prekey_bundles: List[state.PreKeyBundle]):
        self.user_prekey_bundles[user_id] = prekey_bundles

    def get_prekey_bundle(self, user_id) -> state.PreKeyBundle:
        prekey_pool = self.user_prekey_bundles.get(user_id)
        bundle = prekey_pool.pop(0) if prekey_pool else None
        return bundle

    def send_message(self, sender_id, recipient_id, encrypted_message):
        self.message_queue[recipient_id].append((sender_id, encrypted_message))

    def get_messages(self, user_id):
        return self.message_queue.pop(user_id, [])
