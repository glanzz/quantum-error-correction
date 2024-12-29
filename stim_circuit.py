class Circuit:
  def __init__(self):
    self._create()
    self.indent = 0
  
  def _create(self):
    self.program = ""
  
  def print(self):
    '''Prints string representation of the program'''
    print(self.program)

  def _add_to_program(self, inst):
    self.program+= f"{self.indent*' '}{inst}\n"

  
  def reset(self, qubits):
    '''Resets the values of the given qubits useful for rounds of operations'''
    inst = "R"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def x_error(self, probablity, qubits):
    '''Adds bit flip errors on specified qubits with given probablity'''
    inst = self._probablity("X_ERROR", probablity)
    for qubit in qubits:
      inst += f" {qubit}"
    if probablity:
      self._add_to_program(inst)
  
  def tick(self):
    '''Add tick instructions for easy visual representation when viewed using stim library'''
    self._add_to_program("TICK")
  
  def _probablity(self, inst, probablity):
    return f"{inst}({probablity})"
  
  def measure(self, qubits):
    '''Measures the qubits at given list of indices'''
    inst = "M"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def measure_with_reset(self, qubits):
    '''Measures and then resets the qubits at given list of indices'''
    inst = "MR"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def repeat(self, times, func):
    '''Repeats the function block of instructions n times by placing in repeat block'''
    self._add_to_program(f"REPEAT {times}"+"{")
    self.indent += 1
    func()
    self.indent -= 1
    self._add_to_program("}")

  def cx(self, qubits):
    '''Adds CX gate on qubits by consecutive pairing as per the given list of indices'''
    inst = "CX"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def depolarize(self, prob, qubits, single_qubit=False):
    '''Depolarize the qubits at given indices by equally applying operations that corrupt the qubit with given probablity. single_qubit=True applyies single qubit operation, else applies 2 qubit operations.'''
    inst = self._probablity("DEPOLARIZE2" if not single_qubit else "DEPOLARIZE1", prob)
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def detector(self, x, y, register_index, comparision_index=[]):
    '''Add detector at location x,y to spot detection events in the circuit by supplying the indexes in rec register to look for the detection'''
    assert register_index < 0

    inst = f"DETECTOR({x}, {y}) rec[{register_index}]"
    for ci in comparision_index:
      inst += f" rec[{ci}]"
    self._add_to_program(inst=inst)
  
  def shift_coords(self, x, y):
    '''Shift coordinates by qubit(x) and time step(y)'''
    self._add_to_program(f"SHIFT_COORDS({x}, {y})")
  
  def observe(self, index):
    '''Observe the final measurement value from the rec register index given'''
    self._add_to_program(f"OBSERVABLE_INCLUDE(0) rec[{index}]")

    

    
    






    

