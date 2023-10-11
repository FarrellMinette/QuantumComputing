# Import libraries
import numpy as np
import matplotlib.pyplot as plt

# Define the Pauli matrices and other gate matrices
x_matrix = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
y_matrix = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
z_matrix = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
h_matrix = (1/np.sqrt(2)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
cnot_matrix = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 1.0, 0.0]], dtype=complex)
swap_matrix = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]], dtype=complex)
identity_matrix = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]], dtype=complex)

def gate(state, matrix, qubit):
    if(qubit=='0'):
        state[:2, :2] = np.dot(matrix, state[:2, :2])
    elif(qubit=='1'):
        state[2:, :2] = np.dot(matrix, state[2:, :2])
    elif(qubit=='01' or qubit=='10' ):
        state = matrix @ state
        
    return state


# Define a function to apply a sequence of gates to the quantum state
def apply_gate(input_sequence, state, oracle):
    gate_symbols = set('XYZHCSU')  # Define symbols for gate names
    gate_qubit_pairs = input_sequence.split()  # Split input by space
    
    for gate_qubit_pair in gate_qubit_pairs:
        input_gate = ''
        input_qubits = ''
        
        for char in gate_qubit_pair:
            if char in gate_symbols:
                input_gate += char
            elif char.isdigit():
                input_qubits += char
        
        qubit = 0
        matrix = x_matrix
        
        if input_gate in ('X', 'Y', 'Z', 'H'):
            matrix = globals()[f'{input_gate.lower()}_matrix']  # Access the corresponding matrix
        elif input_gate == 'CX':
            matrix = cnot_matrix
        elif input_gate == 'S':
            matrix = swap_matrix
        elif input_gate == 'I':
            matrix = identity_matrix
        elif input_gate == 'U':
            if (oracle=="balanced"): matrix = cnot_matrix
            elif (oracle=="constant"): matrix = identity_matrix
            
        # Apply the gate with the specified qubits
        state = gate(state, matrix=matrix, qubit=input_qubits)

    return state

# Simulate measurements probabilistically
def measurement(state):
    # Calculate the probabilities of measurement outcomes
    prob_00 = np.abs(state[0, 0])**2
    prob_01 = np.abs(state[0, 1])**2
    prob_10 = np.abs(state[1, 0])**2
    prob_11 = np.abs(state[1, 1])**2
    
    probs = [prob_00, prob_01, prob_10, prob_11]
    measurement_outcome = np.random.choice(["00", "01", "10", "11"], p=[prob_00, prob_01, prob_10, prob_11]/sum(probs))
    return measurement_outcome    

def count_measurements(num_iterations, input_sequence, state, oracle="balanced"):
    count_00, count_01, count_10, count_11 = 0, 0, 0, 0

    for iteration in range(num_iterations):
        state = apply_gate(input_sequence, state, oracle)  # Apply the specified gate sequence to the state
        measurement_outcome = measurement(state)
        
        # Update the counts based on the measurement outcome
        if measurement_outcome == "00":
            count_00 += 1
        elif measurement_outcome == "01":
            count_01 += 1
        elif measurement_outcome == "10":
            count_10 += 1
        elif measurement_outcome == "11":
            count_11 += 1

    counts = [count_00, count_01, count_10, count_11]
    outcomes = ['00','01','10','11']    
    print("Measurement Counts:")
    print(counts)
    plt.bar(outcomes, counts)