class QuantumErrorCorrector:
  def __init__(self, distance=5, error_rate=0.001):
    assert distance > 0
    self.distance = (distance*2)-1
    self.error_rate = error_rate
  
  def _create(self):
    self.program = ""

  def _add_to_program(self, inst):
    self.program+= f"{inst}\n"

  def reset_all(self):
    inst = "R"
    for qubit in range(self.distance):
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def reset(self, qubits):
    inst = "R"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def x_error(self, qubits):
    inst = self._probablity("X_ERROR")
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def tick(self):
    self._add_to_program("TICK")
  
  def _probablity(self, inst):
    return f"{inst}({self.error_rate})"
  
  def measure(self, qubits):
    inst = "M"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def repeat(self, times, func):
    self._add_to_program(f"REPEAT {times}"+"{")
    func()
    self._add_to_program("}")

  def cx(self, qubits):
    inst = "CX"
    for qubit in qubits:
      inst += f" {qubit}"
    self._add_to_program(inst)
  
  def depolarize(self, qubits, single_qubit=False):
    inst = self._probablity("DEPOLARIZE2" if not single_qubit else "DEPOLARIZE1")
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



    

  # Move to seperare
  def build_cx_layer(self):
    cx_qubits = list(range(self.distance))[:-1]
    self.cx(cx_qubits)
    self.depolarize(cx_qubits)
    self.depolarize([self.distance-1], single_qubit=True) # 1q depolarize
    self.tick()


    cx_qubits = [x for i in range(2, self.distance, 2) for x in (i, i-1)]
    self.cx(cx_qubits)
    self.depolarize(cx_qubits)
    self.depolarize([0], single_qubit=True)
    self.tick()
  
  # Move to seperare
  def measure_non_data(self, non_data_qubits):
    self.x_error(non_data_qubits)
    self.measure(non_data_qubits)
  

  # Move to seperare
  def build(self):
    self._create()
    self.reset_all()
    self.x_error(range(self.distance))
    self.tick()

    self.build_cx_layer()    

    data_qubits = []
    non_data_qubits = []
    for i in range(self.distance):
      if i % 2 == 0:
        data_qubits.append(i)
      else:
        non_data_qubits.append(i)

    self.measure_non_data(non_data_qubits)
    self.depolarize(data_qubits, single_qubit=True)
    total_non_data_qubits = len(non_data_qubits)
    for i,q in enumerate(non_data_qubits):
        self.detector(q,0,-(total_non_data_qubits-i))
    
    def repitition_layer():
      self.reset(data_qubits)
      self.x_error(data_qubits)
      self.build_cx_layer()
      self.measure_non_data(non_data_qubits)
      self.depolarize(data_qubits, single_qubit=True)
      self.shift_coords(0,1)
      for i,q in enumerate(non_data_qubits):
        self.detector(q,0,-((total_non_data_qubits)-i), [-((2*total_non_data_qubits)-i)])
    
    self.repeat(5, repitition_layer)


    self.x_error(data_qubits)
    self.measure(data_qubits)
    self.shift_coords(0,1)

    total_data_qubits = self.distance - total_non_data_qubits
    for i,q in enumerate(range(total_data_qubits-1)):
        self.detector(q,0,-((total_data_qubits)-i), [-((total_data_qubits)-i-1), -((total_data_qubits)-i+total_non_data_qubits)])
    self.observe(-1)
    
    

    
    






    

