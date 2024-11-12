QIA-foundation-challenge-2024
+++++++++++++++++++++++++++++++++++++++++

introduction
--------------

Welcome to the QIA Foundation Challenge! This repository contains resources and starting code for the challenge.
To participate, please install **SquidASM** (version 0.13 or higher).
`Installation instructions are available here. <https://squidasm.readthedocs.io/en/latest/installation.html>`_

The objective of this challenge is to implement a protocol for **anonymous transmission of classical bits**,
evaluate its error tolerance, and enhance it with a basic form of error correction.

Repository Contents
======================
This repository provides a starting template for the solution code, including:

* *application.py*: A template for the anonymous broadcasting application, with an initialized setup and helper methods.
* *config.yaml*: Configuration for a basic 4-node network (without noise).
* *run_simulation.py*: A script to run and test the application.

Challenge
------------
Your task is to build an application that transmits a byte anonymously, applies error correction,
and then measure the impact of the error correction in the performance in a noisy network.

To help you achieve this, we have defined a series of small, structured goals leading to the final objective.

Goal 1: Implement the Anonymous Bit Transmission Protocol
===========================================================
The first task is to implement the protocol for **anonymous transmission of a classical bit**.
The protocol is described in the `Quantum Anonymous Transmissions paper <https://arxiv.org/pdf/quant-ph/0409201>`_ (see page 10).

For convenience, an image with the protocol definition, *anonymous transmission classical bit.png* is included in this repository.
In this protocol, *d* represents the bit being transmitted anonymously.

To complete this goal, implement the protocol in the *anonymous_transmit_bit* method within *application.py*.
The provided template and helper properties, like *next_node_name*, *prev_node_name*, *next_socket*, etc., that will assist you.


.. note::
    "next" refers to the next node in sequence. For example, for Bob, Charlie is next.
    "prev" refers to the previous node in sequence. For example for Charlie, Bob is prev.

.. note::
    Edge nodes, like Alice and David, have one neighbor only,
    so for Alice "prev" is not applicable and for David "next" is not applicable.
    The associated next or prev properties like *next_socket* or *prev_socket* will be *None* in that case.

.. note::
    The protocol definition specifies aborting if any player doesn’t use the broadcast channel;
    however, implementing this feature is outside the scope of this challenge.

Goal 2: Transmit a Byte Anonymously
======================================
Extend the application to transmit a byte (8 bits) anonymously. Additionally:

* Record the time the application takes to complete.
* In the *run* method, return both the received byte (or sent byte for the sender) and the completion time.

Goal 3: Measure Success Probability and Transmission Speed
==============================================================
Now, calculate the **average success probability** and **transmission speed** in bytes per second.

You can use the *num_times* parameter in the *run* method of *run_simulation.py* to run multiple simulations
and gather data to compute these averages.

Goal 4: Add Error Correction with Repetition Code
===================================================
Implement a basic form of error correction using a `Repetition code <https://en.wikipedia.org/wiki/Repetition_code>`_ of length 3.
Add an option to enable error correction in your application and apply the repetition code for transmitting a single bit anonymously.


Goal 5: Completing the challenge
===================================
To complete the challenge:

1) Configure a Noisy Network:
    *  Modify *config.yaml* to match the **noisy network configuration** settings as described below.
2) Complete the *run_simulation.py* script.
    * Update *run_simulation.py*
        * Execute the application in the noisy network both **with** and **without** error correction.
    * For each configuration:
        * Run the simulation at least 100 times to create reliable results.
        * Calculate and print **Average Success Probability** and **Average Transmission Speed**.
3) Submit your solution
    * Create a GitHub repository containing all necessary files to run your solution script.
    * Register for the QIA Foundation Challenge (if you haven’t already).
    * Email the link to your GitHub repository to info@quantuminternetalliance.org.

Noisy Network configuration
----------------------------
* Nodes:
    * 4-node linear network.
    * Each node spaced 10 km apart.
* Classical Communication:
    * Model: default (to simulate communication delay).
    * Speed: 200,000 km/s in fiber.
* Entanglement Generation:
    * Model: depolarise
    * fidelity: 0.97.
    * Success Probability: 20% per attempt.
* Quantum Device:
    * Model: generic with a 0.5 s coherence time.
    * Gate Operations: 10 μs per operation, with a 0.5% depolarizing error for both single and two-qubit gates.


Hints
-----------

* **SquidASM** provides implementations for `basic functionalities. <https://squidasm.readthedocs.io/en/latest/modules/routines.html>`_
* Use *netsquid.sim_time()* to retrieve the current simulation time in nanoseconds.
* Results from *squidasm.run.stack.run.run*  return as a nested structure:
    * The outer list groups results by node.
    * The inner list contains results per simulation run.
    * Each result is a dictionary, with data returned by the application, with the key names as user specified.
* Network configurations can be generated programmatically using SquidASM’s utility methods. Check the `API <https://squidasm.readthedocs.io/en/latest/modules/util.html>`_ for more information.