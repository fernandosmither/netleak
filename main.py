from simulations.multi_user_sim import MultiUserSimulation


def main():
    num_users = 10
    avg_contacts = 10
    total_messages = 50
    avg_words_per_message = 10

    simulation = MultiUserSimulation(
        num_users, avg_contacts, total_messages, avg_words_per_message
    )
    simulation.run_simulation()


if __name__ == "__main__":
    main()
