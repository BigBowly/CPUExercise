import alu_nocomments as ALU


# the current_register and last_register aren't used
class Register():
  def __init__(self):
    self.table = {'00000': None, '00001': None, '00010': None, '00011': None, '00100': None, '00101': None, '00110': None, '00111': None, '01000': None}
    self.current_register = '00000'
    self.last_register = '00000'


  # moves the current and last register up one. loops upon reaching the last register
  def register_shift(self, register=None):

    if register != None:
      self.current_register = register

    if self.current_register == '00110':
        self.last_register = self.current_register
        self.current_register = '00000'
        return

    self.last_register = self.current_register
    self.current_register = ALU.ADD_parser(self.current_register, '00001')


  # writes to current register if no specific register is entered
  def write(self, value, register=None):
    if register == None:
      print(f"Writing to current register {self.current_register}:{self.table[self.current_register]}")
      self.table[self.current_register] = value 
      self.register_shift()
      return

    else:
      print(f"Writing to specific register {register}:{self.table[register]}")
      self.table[register] = value
      self.register_shift(register)
      return

  # reads from last register if no specific register is entered
  def read(self, register=None):
    if register == None:
      print(f"Reading from current register {self.last_register}:{self.table[self.last_register]}")
      return self.table[self.last_register]
    else:
      print(f"Reading from specific register {register}:{self.table[register]}")
      return self.table[register]
