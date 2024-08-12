import time
import matplotlib.pyplot as plt
from simulations.multi_user_sim import MultiUserSimulation
import pandas as pd
from contextlib import contextmanager


@contextmanager
def time_step(step_name, timings):
    print(f"{step_name}...")
    start_time = time.time()
    yield
    end_time = time.time()
    timings[step_name] = end_time - start_time


def run_simulation_with_timing(num_users, total_messages):
    avg_contacts = 10
    avg_words_per_message = 10

    simulation = MultiUserSimulation(
        num_users, avg_contacts, total_messages, avg_words_per_message
    )

    timings = {}

    # Timing each step
    with time_step("Setting up users", timings):
        simulation.setup_users()

    with time_step("Generating contact lists", timings):
        simulation.generate_contact_lists()

    with time_step("Setting up sessions", timings):
        simulation.setup_sessions()

    with time_step("Simulating messages", timings):
        simulation.simulate_messages()

    with time_step("Printing messages", timings):
        simulation.print_messages()

    total_time = sum(timings.values())
    timings["Total"] = total_time

    return timings


def plot_results(results):
    # Stacked bar chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

    df = pd.DataFrame(results)
    df = df.drop(columns=["Total"])
    df.plot(kind="bar", stacked=True, ax=ax1)
    ax1.set_title("Execution Time Breakdown")
    ax1.set_xlabel("Configuration (num_users, total_messages)")
    ax1.set_ylabel("Time (seconds)")
    ax1.legend(title="Steps", bbox_to_anchor=(1.05, 1), loc="upper left")

    # Total time line plot
    total_times = [result["Total"] for result in results]
    labels = [
        f"({config['num_users']}, {config['total_messages']})" for config in configs
    ]
    ax2.plot(labels, total_times, marker="o")
    ax2.set_title("Total Execution Time")
    ax2.set_xlabel("Configuration (num_users, total_messages)")
    ax2.set_ylabel("Time (seconds)")

    plt.tight_layout()
    plt.savefig("simulation_timing_results.png")
    plt.close()


configs = [
    {"num_users": 10, "total_messages": 50},
    {"num_users": 20, "total_messages": 100},
    {"num_users": 50, "total_messages": 200},
    {"num_users": 100, "total_messages": 500},
    {"num_users": 200, "total_messages": 1000},
    {"num_users": 200, "total_messages": 2000},
    {"num_users": 500, "total_messages": 1000},
    {"num_users": 500, "total_messages": 2000},
]

results = []
for config in configs:
    print(
        f"\nRunning simulation with {config['num_users']} users and {config['total_messages']} messages"
    )
    result = run_simulation_with_timing(**config)
    results.append(result)
    print("Results:", result)

plot_results(results)
print("\nResults have been plotted and saved as 'simulation_timing_results.png'")
