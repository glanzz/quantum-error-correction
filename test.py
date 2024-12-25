from qec_builder import QECBuilder
from stim_circuit import Circuit

builder = QECBuilder(error_rate=0.01, distance=5)
circuit: Circuit = builder.generate()
circuit.print()
