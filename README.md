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
   Generate and distribute the entangled state $(|0^n\rangle + |1^n\rangle) / \sqrt{2}$ among all participants (including Alice).
   I used a GHZ state using function 

   `create_ghz(
            connection,
            self.prev_epr_socket,
            self.next_epr_socket,
            self.prev_socket,
            self.next_socket,
            do_corrections=True,
        )`
   

   A **GHZ state** (named after Greenberger, Horne, and Zeilinger) is a special type of entangled state in quantum mechanics that involves three or more qubits. It is represented as a superposition of states where **all qubits are either in the $ |0\rangle $ state or all in the $ |1\rangle $ state**.
   For three qubits, the GHZ state is written as:

   
   $|\text{GHZ}\rangle = \frac{1}{\sqrt{2}}(|000\rangle + |111\rangle)$
   

   This state means that each qubit is entangled with the others in such a way that, when one qubit is measured, the measurement result immediately determines the state of the other qubits. For example, if you measure one qubit and get a 0, then you know the other qubits are also in the 0 state. Similarly, if you measure a 1, all other qubits will also be in the 1 state.
   For **n** qubits, the GHZ state generalizes to:

   $|\text{GHZ}\rangle = \frac{1}{\sqrt{2}}(|0\rangle^{\otimes n} + |1\rangle^{\otimes n}) $

   This state can be used to create strongly correlated outcomes across multiple qubits and is fundamental in tests of quantum nonlocality and for quantum protocols requiring synchronized behavior.

2. **Alice's Phase Flip Operation**
   - Alice sets her bit $d$.
   - If $d = 1$, she applies the phase flip $\sigma_z$ (Pauli-Z gate) to her part of the entangled state.
   - If $d = 0$, she does nothing.

3. **Each Participant's Operations (Including Alice)**
     - Applies a Hadamard transform to their qubit.
     - Measures their qubit in the computational $Z$ basis.
     - Broadcasts their measurement result (either '0' or '1') to all other participants.

4. **Counting and Conclusion**
   - All participants collect the broadcasted measurement results.
   - Count the total number of '1's, denoted as $k$.
   - If $k$ is even, conclude that $d = 0$; if $k$ is odd, conclude that $d = 1$.
### Task 2️⃣: Transmit a Byte Anonymously
> Extend the application to transmit a byte (8 bits) anonymously. Additionally:
> Record the time the application takes to complete.
> In the run method, return both the received byte (or sent byte for the sender) and the completion time.

I created `application_onebit.py` and  `config_onebit.yaml` to distinguish between the one bit and one byte implementations.

### Task 3️⃣: Measure Success Probability and Transmission Speed
> Now, calculate the average success probability and transmission speed in bytes per second.
> You can use the num_times parameter in the run method of run_simulation.py to run multiple simulations and gather data to compute these averages.

$Average-success-probability = (\frac{bit-sended-right} {total-bits}) * 100$

$Transmission-Speed= mean(sim-times)$
### Task 4️⃣: Add Error Correction with Repetition Code
> Implement a basic form of error correction using a Repetition code of length 3. Add an option to enable error correction in your application and apply the repetition code for transmitting a single bit anonymously.

Basically, we replicate the bit sended three times (for bit $1$ we do $111$), and then we calculate the most recurring bit in a group of three bits.
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

I saved two log files with the average success probability and sim_time, so you'll be able to see the different results


