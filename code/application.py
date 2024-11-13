from copy import copy, deepcopy
from typing import Optional, Generator

from netqasm.sdk import Qubit
from netqasm.sdk.toolbox import set_qubit_state
from netqasm.sdk.qubit import QubitMeasureBasis

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.epr_socket import EPRSocket

from netsquid.util.simtools import sim_time, MILLISECOND


class AnonymousTransmissionProgram(Program):
    def __init__(self, node_name: str, node_names: list, send_bit: bool = None):
        """
        Initializes the AnonymousTransmissionProgram.

        :param node_name: Name of the current node.
        :param node_names: List of all node names in the network, in sequence.
        :param send_bit: The bit to be transmitted; set to None for nodes that are not the sender.
        """
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
        received_bit = yield from self.anonymous_transmit_bit(context, self.send_bit)

        print(f"{self.node_name} has received the bit: {received_bit}")
        return {}

    def anonymous_transmit_bit(self, context: ProgramContext, send_bit: bool = None) -> Generator[None, None, bool]:
        """
        Anonymously transmits a bit to other nodes in the network as part of the protocol.

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
        #Step 1: shared state
        connection = context.connection
        
        if send_bit:
            #Step 1: shared state
            #d = self.create_super_state(connection)

            
            #d = self.next_epr_socket.create_keep()[0]
            #shared = d.measure()
            shared =1
            yield from connection.flush()
            
            
            
            q = Qubit(connection)
            #Step 2: Alice applies Pauli-Z if the condition is met
            if shared == 1: 
                #set the qubit state to zero (should be the default)
                q.reset()
                #set the qubit to one using 
                q.X()
                #Alice applies the Pauli-Z Gate
                q.Z()

            #step 3: what everybody ha to do
            #every player applies the hadamard port 
            q.H()
            #every player has to measure in computational basis (should be the default, but we like to specify)
            src = q.measure(basis=QubitMeasureBasis.Z)
            yield from connection.flush()
            #broadcast 
            self.broadcast_message(context, str(src))
            #step 4: count occurences
            
            #returns d, as defined in the protocol (2.5)
            return str(src).count('1') % 2 == 0
        
        
        #This code is for Bob, Charlie and David
        else:
            '''
            idea per domani: prendi la misurazione da next socket
            se funzionasse il broadcast, e dovrebbe, il dato è già lì!
            '''
            #q = yield from self.prev_epr_socket.recv_keep()
            #if self.next_epr_socket is not None:
                #u = self.next_epr_socket.create_keep()[0]
            #every player applies the hadamard port 
            q = Qubit(connection)
            
            q.H()
            #every player has to measure in computational basis (should be the default, but we like to specify)
            src = q.measure(basis=QubitMeasureBasis.Z)
            
            yield from connection.flush()
            '''
            u.reset()
            if src == 1: 
                u.X()
                '''
            #broadcast 
            self.broadcast_message(context, str(src))
            msg = yield from self.prev_socket.recv()
            
            return msg.join(str(src)).count('1') % 2 == 0
            
            
                

        #end code
        yield from connection.flush()
        return False
        
    def create_super_state(self, connection):
        qubits = [Qubit(connection) for _ in range(2)]
        for i in range(2): 
            set_qubit_state(qubits[i])
        qubits[0].H()
        qubits[0].cnot(qubits[1])
        return qubits[0]    
            
        
    def broadcast_message(self, context: ProgramContext, message: str):
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
