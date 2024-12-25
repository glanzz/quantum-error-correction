class Circuit:
  def __init__(self):
    self._create()
    self.indent = 0
  
  def _create(self):
    self.program = ""
  
  def print(self):
    print(self.program)

  def _add_to_program(self, inst):
    self.program+= f"{self.indent*' '}{inst}\n"

  
  def reset(self, qubits):
    inst = "R"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def x_error(self, probablity, qubits):
    inst = self._probablity("X_ERROR", probablity)
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def tick(self):
    self._add_to_program("TICK")
  
  def _probablity(self, inst, probablity):
    return f"{inst}({probablity})"
  
  def measure(self, qubits):
    inst = "M"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def repeat(self, times, func):
    self._add_to_program(f"REPEAT {times}"+"{")
    self.indent += 1
    func()
    self.indent -= 1
    self._add_to_program("}")

  def cx(self, qubits):
    inst = "CX"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def depolarize(self, prob, qubits, single_qubit=False):
    inst = self._probablity("DEPOLARIZE2" if not single_qubit else "DEPOLARIZE1", prob)
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def detector(self, x, y, register_index, comparision_index=[]):
    assert register_index < 0

    inst = f"DETECTOR({x}, {y}) rec[{register_index}]"
    for ci in comparision_index:
      inst += f" rec[{ci}]"
    self._add_to_program(inst=inst)
  
  def shift_coords(self, x, y):
    self._add_to_program(f"SHIFT_COORDS({x}, {y})")
  
  def observe(self, index):
    self._add_to_program(f"OBSERVABLE_INCLUDE(0) rec[{index}]")

    

    
    






    

