from typing import Optional
from signal_protocol import (
    curve,
    identity_key,
    state,
    storage,
    session,
    session_cipher,
    address,
)
import uuid
import secrets
import time
import logging
from .utils import generate_unique_id

logging.basicConfig(level=logging.DEBUG)


class SignalClient:
    def __init__(
        self,
        user_id: Optional[str] = None,  # str | None
        pre_key_pool_size=1,
    ):
        self.user_id = user_id or str(uuid.uuid4())
        self.address = address.ProtocolAddress(self.user_id, 1)  # Using device ID 1
        self.identity_key_pair = identity_key.IdentityKeyPair.generate()
        self.registration_id = self._generate_registration_id()
        self.store = storage.InMemSignalProtocolStore(
            self.identity_key_pair, self.registration_id
        )
        self.pre_key_bundles = [
            self._generate_pre_key_bundle() for _ in range(pre_key_pool_size)
        ]

    def _generate_registration_id(self):
        return secrets.randbelow(16380) + 1  # Generates a number between 1 and 16380

    def _generate_pre_key_bundle(self):
        pre_key_pair = curve.KeyPair.generate()
        signed_pre_key_pair = curve.KeyPair.generate()
        signed_pre_key_public = signed_pre_key_pair.public_key().serialize()
        signed_pre_key_signature = (
            self.identity_key_pair.private_key().calculate_signature(
                signed_pre_key_public
            )
        )

        pre_key_id = generate_unique_id()
        signed_pre_key_id = generate_unique_id()

        pre_key_record = state.PreKeyRecord(pre_key_id, pre_key_pair)
        self.store.save_pre_key(pre_key_id, pre_key_record)

        signed_pre_key_record = state.SignedPreKeyRecord(
            signed_pre_key_id,
            int(time.time() * 1000),  # Current timestamp in milliseconds
            signed_pre_key_pair,
            signed_pre_key_signature,
        )
        self.store.save_signed_pre_key(signed_pre_key_id, signed_pre_key_record)

        return state.PreKeyBundle(
            self.registration_id,
            1,  # device id
            pre_key_id,
            pre_key_pair.public_key(),
            signed_pre_key_id,
            signed_pre_key_pair.public_key(),
            signed_pre_key_signature,
            self.identity_key_pair.identity_key(),
        )

    def add_new_prekey_bundle(self) -> state.PreKeyBundle:
        self.pre_key_bundles.append(self._generate_pre_key_bundle())
        return self.pre_key_bundles[-1]

    def process_prekey_bundle(self, recipient_id, prekey_bundle):
        recipient_address = address.ProtocolAddress(
            recipient_id, 1
        )  # Using device ID 1
        # logging.debug(f"Processing prekey bundle for {recipient_id}")
        try:
            session.process_prekey_bundle(recipient_address, self.store, prekey_bundle)
        except Exception as e:
            # logging.error(f"Error processing prekey bundle for {recipient_id}: {e}")
            pass

    def encrypt_message(self, recipient_id, message):
        recipient_address = address.ProtocolAddress(
            recipient_id, 1
        )  # Using device ID 1
        return session_cipher.message_encrypt(
            self.store, recipient_address, message.encode()
        )

    def decrypt_message(self, sender_id, encrypted_message):
        sender_address = address.ProtocolAddress(sender_id, 1)  # Using device ID 1
        return session_cipher.message_decrypt(
            self.store, sender_address, encrypted_message
        ).decode()

    def send_message_to_many(self, recipient_ids, message):
        encrypted_messages = {}
        for recipient_id in recipient_ids:
            encrypted_messages[recipient_id] = self.encrypt_message(
                recipient_id, message
            )
        return encrypted_messages
