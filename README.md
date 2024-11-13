# Welcome!✨
This is my entry for [Quantum Internet Application Challenge 2024](https://github.com/QuTech-Delft/QIA-foundation-challenge-2024/?tab=readme-ov-file), the objective of this challenge is to implement an **Anonymous Bit Transmission Protocol** Using [SquidASM](https://squidasm.readthedocs.io/en/latest/installation.html). 
### how did I manage to implement this protocol?🧐
Firstly, I've read all the documentation and watched the provided [tutorials about SquidASM](https://www.youtube.com/watch?v=LwDG3ecU24s&list=PL5jmbd6SJYnMW3p28I5CUBK8kC6b9wHjs&index=3), [the paper provided by QIA foundation](https://arxiv.org/pdf/quant-ph/0409201) and the [image provided](https://github.com/mariacaterinadaloia/QIA_foundation_challenge_DAloia/blob/main/code/anonymous%20transmission%20classical%20bit.png) to explain the structure of the requested protocol. 
## 💡Anonymous Bit Transmission Protocol💡
The initial structure is provided on the GitHub repository already linked. The challenge is divided in tasks, below I report every task present in the link above and how I completed it.
### Task 1️⃣: Implement the Anonymous Bit Transmission Protocol
> The first task is to implement the protocol for anonymous transmission of a classical bit. The protocol is described in the Quantum Anonymous Transmissions paper (see page 10).
> For convenience, an image with the protocol definition, anonymous transmission classical bit.png is included in this repository. In this protocol, d represents the bit being transmitted anonymously.
> To complete this goal, implement the protocol in the anonymous_transmit_bit method within application.py. The provided template and helper properties, like next_node_name, prev_node_name, next_socket, etc., that will assist you.

I firstly divided the code into 5 steps:

#### **Implementation Steps for ANON(d)**

1. **Prerequisite: Prepare Shared State**
   Generate and distribute the entangled state \((|0^n\rangle + |1^n\rangle) / \sqrt{2}\) among all participants (including Alice).

2. **Alice's Phase Flip Operation**
   - Alice sets her bit \(d\).
   - If \(d = 1\), she applies the phase flip \(\sigma_z\) (Pauli-Z gate) to her part of the entangled state.
   - If \(d = 0\), she does nothing.

3. **Each Participant's Operations (Including Alice)**
     - Applies a Hadamard transform to their qubit.
     - Measures their qubit in the computational (Z) basis.
     - Broadcasts their measurement result (either '0' or '1') to all other participants.

4. **Counting and Conclusion**
   - All participants collect the broadcasted measurement results.
   - Count the total number of '1's, denoted as \(k\).
   - If \(k\) is even, conclude that \(d = 0\); if \(k\) is odd, conclude that \(d = 1\).
### Task 2️⃣: Transmit a Byte Anonymously
> Extend the application to transmit a byte (8 bits) anonymously. Additionally:
> Record the time the application takes to complete.
> In the run method, return both the received byte (or sent byte for the sender) and the completion time.
### Task 3️⃣: Measure Success Probability and Transmission Speed
> Now, calculate the average success probability and transmission speed in bytes per second.
> You can use the num_times parameter in the run method of run_simulation.py to run multiple simulations and gather data to compute these averages.
### Task 4️⃣: Add Error Correction with Repetition Code
> Implement a basic form of error correction using a Repetition code of length 3. Add an option to enable error correction in your application and apply the repetition code for transmitting a single bit anonymously.
### Task 5️⃣: Completing the challenge
> To complete the challenge:
> Configure a Noisy Network:
>   Modify config.yaml to match the noisy network configuration settings as described below.
>   Complete the run_simulation.py script.
> Update run_simulation.py
> Execute the application in the noisy network both with and without error correction.
> For each configuration:
>   Run the simulation at least 100 times to create reliable results.
>   Calculate and print Average Success Probability and Average Transmission Speed.



