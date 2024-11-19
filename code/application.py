from copy import copy, deepcopy
from typing import Optional, Generator


from netqasm.sdk import Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.toolbox import set_qubit_state
from netqasm.sdk.qubit import QubitMeasureBasis
import random

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.epr_socket import EPRSocket
from squidasm.util.routines import create_ghz

from netsquid.util.simtools import sim_time, SECOND


class AnonymousTransmissionProgram(Program):
    def __init__(self, node_name: str, node_names: list, send_bit: bool = None, repetition_code = False):
        """
        Initializes the AnonymousTransmissionProgram.

        :param node_name: Name of the current node.
        :param node_names: List of all node names in the network, in sequence.
        :param send_bit: The bit to be transmitted; set to None for nodes that are not the sender.
        """
        self.simtime = None
        self.final = ""
        self.node_name = node_name
        self.send_bit = send_bit

        # Find what nodes are next and prev based on the node_names l ist
        node_index = node_names.index(node_name)
        self.next_node_name = node_names[node_index+1] if node_index + 1 < len(node_names) else None
        self.prev_node_name = node_names[node_index-1] if node_index - 1 >= 0 else None

        # The remote nodes are all the nodes, but without current node. Copy the list to make the pop operation local
        self.remote_node_names = copy(node_names)
        self.remote_node_names.pop(node_index)

        # next and prev sockets, will be fetched from the ProgramContext using setup_next_and_prev_sockets
        self.next_socket: Optional[Socket] = None
        self.next_epr_socket: Optional[EPRSocket] = None
        self.prev_socket: Optional[Socket] = None
        self.prev_epr_socket: Optional[EPRSocket] = None

    @property
    def meta(self) -> ProgramMeta:
        # Filter next and prev node name for None values
        epr_node_names = [node for node in [self.next_node_name, self.prev_node_name] if node is not None]

        return ProgramMeta(
            name="anonymous_transmission_program",
            csockets=self.remote_node_names,
            epr_sockets=epr_node_names,
            max_qubits=2,
        )

    def run(self, context: ProgramContext):
        # Initialize next and prev sockets using the provided context
        self.setup_next_and_prev_sockets(context)

        # Run the anonymous transmission protocol and retrieve the received bit
        received_byte = yield from self.anonymous_transmit_bit(context, self.send_bit)

        print(f"{self.node_name} has received the bit: {received_byte}")
        self.simtime = sim_time(SECOND)
        return {}

    def anonymous_transmit_bit(self, context: ProgramContext, send_bit: bool = None, repetition_code = False) -> Generator[None, None, bool]:
        """
        Anonymously transmits a byte to other nodes in the network as part of the protocol.

        :param context: The program's execution context.
        :param send_bit: Bit to be sent by the sender node; receivers should leave this as None.
        :return: The bit received through the protocol, or the sent bit if this node is the sender.
        """
        #Start code
        '''
        To make the development easier, i divided the protocol into steps, 
        they will be specified throughout the entire code. 
        In the README.md you can find the logic behind! 
        '''
        self.final = ""
        #Step 1: shared state
        connection = context.connection
        #creating a GHZ state

        for i in range(8):
            q, m = yield from create_ghz(
                connection,
                self.prev_epr_socket,
                self.next_epr_socket,
                self.prev_socket,
                self.next_socket,
                do_corrections=True,
            )

            yield from connection.flush()
            #if Alice
            if send_bit:
                shared = random.choice([0,1])
                #Step 2: Alice applies Pauli-Z if the condition is met
                if shared == 1:
                    #Alice applies the Pauli-Z Gate
                    q.Z()
            #Step 3: what everybody ha to do
            #applies the hadamard port to the shared state
            q.H()
            # every player has to measure in computational basis (should be the default, but we like to specify)
            src = q.measure(basis=QubitMeasureBasis.Z)
            yield from connection.flush()

            #broadcast
            msg = StructuredMessage(str(i), "")

            if self.prev_socket is not None:
                msg = yield from self.prev_socket.recv()
                if str(i) not in msg.header:
                    while True:
                        msg = yield from self.prev_socket.recv()
                        if str(i) in msg.header:
                            break

            msg_str = str(msg.payload) + str(src)

            if repetition_code:
                _, msg_str = self.repetition_code_func(msg.payload, src)
                if self.next_socket is not None:
                    self.broadcast_message(context, StructuredMessage(str(i), msg_str))
                else:
                    self.broadcast_message(context, StructuredMessage(str(i), ""))

                self.final = self.final + self.repetition_code_func(msg)

            else:
                if self.next_socket is not None:
                    self.broadcast_message(context, StructuredMessage(str(i), msg_str))
                else:
                    self.broadcast_message(context, StructuredMessage(str(i), ""))

                if str(msg_str).count('1') % 2 != 0:
                    self.final = self.final + "1"
                else:
                    self.final = self.final + "0"

        return self.final

    def repetition_code_func(self, input_string, src = None):
        result_string = ""
        for i in range(0, len(input_string), 3):
            group = input_string[i:i + 3]

            count_ones = group.count('1')

            if count_ones >= 2:
                result_string += "1"
            else:
                result_string += "0"
        if src is not None:
            to_send = input_string + str(src) + str(src) + str(src)
        return result_string, to_send

    def broadcast_message(self, context: ProgramContext, message: StructuredMessage):
        """Broadcasts a message to all nodes in the network."""        
        for remote_node_name in self.remote_node_names:
            socket = context.csockets[remote_node_name]
            socket.send(message)
             

    def setup_next_and_prev_sockets(self, context: ProgramContext):
        """Initializes next and prev sockets using the given context."""
        if self.next_node_name:
            self.next_socket = context.csockets[self.next_node_name]
            self.next_epr_socket = context.epr_sockets[self.next_node_name]
        if self.prev_node_name:
            self.prev_socket = context.csockets[self.prev_node_name]
            self.prev_epr_socket = context.epr_sockets[self.prev_node_name]
