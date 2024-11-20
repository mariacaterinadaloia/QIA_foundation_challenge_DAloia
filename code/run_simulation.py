from numpy import mean

from application import AnonymousTransmissionProgram

from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run

log_file = "simulation.log"
#for error correction enabled
#log_file = "simulation_correction.log"
# Open the file in write mode to clear its content
with open(log_file, "w") as f:
    pass  # Opening in "w" mode clears the file
nodes = ["Alice", "Bob", "Charlie", "David"]

# import network configuration from file
cfg = StackNetworkConfig.from_file("config.yaml")

# Create instances of programs to run
alice_program = AnonymousTransmissionProgram(node_name="Alice", node_names=nodes, send_bit=True)#repetition_code=True)
bob_program = AnonymousTransmissionProgram(node_name="Bob", node_names=nodes)#repetition_code=True)
charlie_program = AnonymousTransmissionProgram(node_name="Charlie", node_names=nodes)# repetition_code=True)
david_program = AnonymousTransmissionProgram(node_name="David", node_names=nodes)# repetition_code=True)

num_times = 100
for i in range(num_times):
    # Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
    run(config=cfg, programs={"Alice": alice_program, "Bob": bob_program,
                              "Charlie": charlie_program, "David": david_program}, num_times=1)
    results = [alice_program.final, bob_program.final, charlie_program.final, david_program.final]


    total_matches = 0
    reference = results[0]
    byte_success = []
    for j in range(1, len(results)):
        correct_bits = sum(1 for k in range(8) if results[j][k] != reference[k])
        byte_success.append(correct_bits)
    average_success = 8 - mean(byte_success)
    average_success_rate = (average_success / 8) * 100

    sim_times = [bob_program.simtime - alice_program.simtime , charlie_program.simtime - alice_program.simtime, david_program.simtime - alice_program.simtime]
    print(f"Average success rate: {average_success_rate} and Average Transmission Speed: {mean(sim_times)}")

    with open(log_file, "a") as f:  # Open the file in append mode
        f.write(
            f"Average success rate: {average_success_rate} and Average Transmission Speed: {mean(sim_times)}\n")



