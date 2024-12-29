# Quantum Error Correction API

API for Stim quantum error correction circuits
The repository offers a quick circuit class API to build stim circuit for quantum error correction.

### Usage

```python
from stim_circuit import Circuit
data_qubits = [1, 3, 5]
non_data_qubits = [0, 2, 4]
circuit = Circuit()
circuit.reset([*data_qubits, *non_data_qubits])
circuit.x_error(0.001, non_data_qubits)
circuit.measure(non_data_qubits)

print(circuit.program) # Prints the circuit string in stim format
```

The API also provides other various operations offered by stim cx, depolarize, etc as shown below:

- `circuit.reset(qubits)`: resets the qubits at given list of indices
- `circuit.print()`: Prints string representation of the stim program
- `circuit.x_error(probablity=0.001, qubits=[0,1])`: Adds bit flip errors with given probablity to qubits at given list of indices
- `circuit.tick()`: Add tick instructions for easy visual representation when viewed using stim library
- `circuit.measure(qubits=[0,3])`: Measures the qubits at given list of indices
- `circuit.measure_with_reset(qubits=[0,3])`: Measures and then resets the qubits at given list of indices
- `circuit.repeat(times=3, func=apply_cx_operation)`: Repeats the custom defined function n times which are block of instructions, by placing in repeat block
- `circuit.cx(qubits=[0,1,2,3])`: Adds CX gate on qubits by consecutive pairing as per the given list of indices, the list should have even number of elements
- `circuit.depolarize(probablity=0.01, qubits=[0,1,2,3], single_qubit=False)`: Depolarize the qubits at given indices by equally applying operations that corrupt the qubit with given probablity. single_qubit=True applies single qubit operation, else applies 2 qubit operations.
- `circuit.depolarize(probablity=0.01, qubits=[0,1,2,3], single_qubit=False)`: Depolarize the qubits at given indices by equally applying operations that corrupt the qubit with given probablity. single_qubit=True applies single qubit operation, else applies 2 qubit operations.
- `circuit.shift_coords(x=0,y=1)`: Shift coordinates by qubit(x) and time step(y)
- `circuit.observe(index=0)`: Observe the final measurement value from the rec register at givenindex


### Importing into stim for further analysis

```python
from stim_circuit import Circuit
import stim as s

qec = Circuit()
qec.reset([0,1,2,3,4,5])
qec.x_error(0.001, [1,2,3,4])
qec.measure([1,2,3,4])
circuit = s.Circuit(qec.program)
sampler = circuit.compile_sampler()
print(sampler.sample(shots=10))
```


### Realistic quantum model
Check QECBuilder to build a realistic quantum error correction circuit for given code distance and physical error probablities