from stim_circuit import Circuit
class QECBuilder:
  def __init__(self, distance=5, error_rate=0.001):
    assert distance > 0
    self.distance = (distance*2)-1
    self.error_rate = error_rate


  
  def build_cx_layer(self):
    cx_qubits = list(range(self.distance))[:-1]
    self.circuit.cx(cx_qubits)
    self.circuit.depolarize(self.error_rate, cx_qubits)
    self.circuit.depolarize(self.error_rate, [self.distance-1], single_qubit=True) # 1q depolarize
    self.circuit.tick()


    cx_qubits = [x for i in range(2, self.distance, 2) for x in (i, i-1)]
    self.circuit.cx(cx_qubits)
    self.circuit.depolarize(self.error_rate, cx_qubits)
    self.circuit.depolarize(self.error_rate, [0], single_qubit=True)
    self.circuit.tick()
  
  def measure_non_data(self, non_data_qubits):
    self.circuit.x_error(self.error_rate, non_data_qubits)
    self.circuit.measure(non_data_qubits)

  def __seperate_qubits(self):
    self.data_qubits = []
    self.non_data_qubits = []
    for i in range(self.distance):
      if i % 2 == 0:
        self.data_qubits.append(i)
      else:
        self.non_data_qubits.append(i)

  def __initalize_build(self):
    self.circuit.reset(range(self.distance))
    self.circuit.x_error(self.error_rate, range(self.distance))
    self.circuit.tick()
  
  def __build_core_layer(self):
    self.build_cx_layer()
    self.measure_non_data(self.non_data_qubits)
    self.circuit.depolarize(self.error_rate, self.data_qubits, single_qubit=True)
  
  def __add_single_detectors(self):
    total_non_data_qubits = len(self.non_data_qubits)
    for i,q in enumerate(self.non_data_qubits):
        self.circuit.detector(q,0,-(total_non_data_qubits-i))
  
  def __build_repitition_layer(self):
      total_non_data_qubits = len(self.non_data_qubits)
      self.circuit.reset(self.data_qubits)
      self.circuit.x_error(self.error_rate, self.data_qubits)
      self.__build_core_layer()
      self.circuit.shift_coords(0,1)
      for i,q in enumerate(self.non_data_qubits):
        self.circuit.detector(q,0,-((total_non_data_qubits)-i), [-((2*total_non_data_qubits)-i)])

  def __build_final_layer(self):
      self.circuit.x_error(self.error_rate, self.data_qubits)
      self.circuit.measure(self.data_qubits)
      self.circuit.shift_coords(0,1)

      total_non_data_qubits = len(self.non_data_qubits)
      total_data_qubits = self.distance - total_non_data_qubits
      for i,q in enumerate(range(total_data_qubits-1)):
          self.circuit.detector(self.non_data_qubits[i],0,-((total_data_qubits)-i), [-((total_data_qubits)-i-1), -((total_data_qubits)-i+total_non_data_qubits)])
      self.circuit.observe(-1)
  

  def __build_initial_layer(self):
    self.__initalize_build()
    self.__build_core_layer()
    self.__add_single_detectors()


  def build(self):
    self.circuit:Circuit = Circuit()
    self.__seperate_qubits()
    self.__build_initial_layer()
    self.circuit.repeat(5, self.__build_repitition_layer)
    self.__build_final_layer()
  
  def generate(self):
    self.build()
    return self.circuit
    

    
    
    

    
    






    

