import random
from typing import Dict, Set
import numpy as np
from collections import defaultdict
from signal_client.client import SignalClient
from server.server import SignalServer
from nltk.corpus import words
import nltk


class MultiUserSimulation:
    """
    Consider that the average contacts per user will be a little higher than
    avg_contacts due to the bidirectional nature of the simulation.
    """

    def __init__(
        self,
        num_users: int,
        avg_contacts: int,
        total_messages: int,
        avg_words_per_message: int,
    ):
        self.num_users = num_users
        self.avg_contacts = avg_contacts
        self.total_messages = total_messages
        self.avg_words_per_message = avg_words_per_message
        self.server = SignalServer()
        self.clients: Dict[str, SignalClient] = {}
        self.contact_lists: Dict[str, Set[str]] = defaultdict(set)
        try:
            self.word_list = words.words()
        except LookupError:
            nltk.download("words")
            self.word_list = words.words()

    def setup_users(self):
        for i in range(self.num_users):
            user_id = f"user_{i}"
            client = SignalClient(user_id, pre_key_pool_size=self.num_users)
            self.clients[user_id] = client
            self.server.register_user(client.user_id, client.pre_key_bundles)

    def generate_contact_lists(self):
        for user_id, client in self.clients.items():
            num_contacts = max(
                1, int(np.random.normal(self.avg_contacts, self.avg_contacts / 3))
            )
            potential_contacts = list(set(self.clients.keys()) - {user_id})
            contacts = random.sample(
                potential_contacts, min(num_contacts, len(potential_contacts))
            )
            for contact in contacts:
                self.contact_lists[user_id].add(contact)
                self.contact_lists[contact].add(user_id)

    def setup_sessions(self):
        for user_id, contacts in self.contact_lists.items():
            for contact in contacts:
                prekey_bundle = self.server.get_prekey_bundle(contact)
                self.clients[user_id].process_prekey_bundle(contact, prekey_bundle)

    def generate_random_message(self):
        num_words = max(
            1,
            int(
                np.random.normal(
                    self.avg_words_per_message, self.avg_words_per_message / 3
                )
            ),
        )
        return " ".join(random.choice(self.word_list) for _ in range(num_words))

    def simulate_messages(self):
        for _ in range(self.total_messages):
            sender = random.choice(list(self.clients.keys()))
            if not self.contact_lists[sender]:
                continue
            recipient = random.choice(list(self.contact_lists[sender]))
            message = self.generate_random_message()

            encrypted_message = self.clients[sender].encrypt_message(recipient, message)
            self.server.send_message(sender, recipient, encrypted_message)

    def print_messages(self):
        for user_id, client in self.clients.items():
            print(f"\nMessages for {user_id}:")
            messages = self.server.get_messages(user_id)
            for sender_id, enc_message in messages:
                decrypted_message = client.decrypt_message(sender_id, enc_message)
                print(f"From {sender_id}: {decrypted_message}")

    def run_simulation(self):
        print("Setting up users...")
        self.setup_users()

        print("Generating contact lists...")
        self.generate_contact_lists()

        print("Setting up sessions...")
        self.setup_sessions()

        print("Simulating messages...")
        self.simulate_messages()

        print("Simulation complete. Printing messages:")
        self.print_messages()
