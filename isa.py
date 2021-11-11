import alu_nocomments as ALU
import memory as MEM
import register as REG


# init function for the ISA
# holds the opcodes, functions, and connections to the other processor components
class ISA():
  def __init__(self):
    self.opcodes = {'001100': self.store_r, '001101': self.load_r, '001000': self.store_m, '001001': self.load_m, '011001': self.jump, '011011': self.show_output}
    self.functions = {'000001': self.alu_add, '000010': self.alu_sub, '000011': self.alu_mult, '000100': self.alu_div}
    self.cache = MEM.Cache()
    self.main_memory = MEM.Main_Memory()
    self.register = REG.Register()
    self.output = ''
    self.overflow = 0
    self.function_identifier = [['Addition', None, None], ['Subtraction', None, None], ['Multiplication', None, None], ['Division', None, None]]
    self.function_index = None


  # some utility functions
  # makes sure bit length meets the 32 bit requirement
  # spaces are removed from the instructions
  # alters the function lists to print the correct arthmetic information

  def remove_spaces(self, line):
    new_line = ''
    for char in line:
      if char != ' ':
        new_line += char

    return new_line

  def alter_bit_length(self,num):
    if len(num) < 32:
      add_len = 32 - len(num)
      num = (add_len * '0') + num
      return num
    elif len(num) > 32:
      print(f"something went wrong: number shouldn't be that long")
      return
    else:
      return num

  def alter_function(self, arg1, arg2):
    self.function_identifier[self.function_index][1] = ALU.remove_num_len(arg1)
    self.function_identifier[self.function_index][2] = ALU.remove_num_len(arg2)


  # reads the instruction file and weeds out the spaces and comments leaving only 32 bit binary lines
  def instruction_reader(self, file):
    with open(file) as codefile:
      code = codefile.readlines()
      lines = [line.strip() for line in code if line.strip() != '']
      lines = [line.rstrip() for line in lines]
      lines = [line for line in lines if line[0] != "#"]
      lines = [self.remove_spaces(line) for line in lines]

      if len(lines) == None:
        print(f"There were no instructions.")
        return
      else:
        for line in lines:
          self.line_parser(line)

    return

  # takes the altered lines and reads the binary opcodes, register numbers, binary numbers and function 
  # codes to determine if numbers need to be stored or retrieved, or whether binary calculations need
  # to be processed 
  def line_parser(self, line):
    opcode = line[:6]
    r1 = ''
    r2 = ''
    dr = ''
    shift = ''
    function = ''
    num = ''

    # arithmetic
    if opcode == '000010':
      r1 = line[6:11]
      r2 = line[11:16]
      dr = line[16:21]
      shift = line[21:26]
      function = line[26:32]
      if function in list(self.functions.keys()):
        if function == '000001':
          self.function_index = 0
          self.alu_add(r1, r2, dr)
        elif function == '000010':
          self.function_index = 1
          self.alu_sub(r1, r2, dr)
        elif function == '000011':
          self.function_index = 2
          self.alu_mult(r1, r2, dr)
        elif function == '000100':
          self.function_index = 3
          self.alu_div(r1, r2, dr)

    # register storage
    elif opcode == '001100':
      # register
      r1 = line[6:11]
      # number
      num = self.alter_bit_length(line[11:32])
      self.store_r(r1, num)

    # register retrieval
    elif opcode == '001101':
      # register
      r1 = line[6:11]
      self.load_r(r1)

    # memory storage
    elif opcode == '001000':
      # register
      r1 = line[6:11]
      # mem address
      r2 = line[11:16]
      self.store_m(r2, r1)

    # memory retrieval
    elif opcode == '001001':
      # mem address
      r1 = line[6:11]
      # destination register
      r2 = line[11:16]
      self.load_m(r1, r2)

    # answer storage
    elif opcode == '011001':
      # register
      r1 = line[6:11]
      self.jump(r1)

    # printing of answer
    elif opcode == '011011':
      self.show_output()

    else:
      print(f"No such opcode")
      return



  # register storage - (register, data)
  def store_r(self, arg1, arg2):
    print(f"Writing {arg2} into register {arg1}")
    # (data, register)
    self.register.write(arg2, arg1)


  # memory storage - (memory address, data)
  def store_m(self, arg1, arg2):
    # makes sure the stored value is always 32 bits
    num = self.alter_bit_length(self.register.read(arg2))
    print(f"Writing data - {num} into cache address - {arg1}")
    result = self.cache.write(arg1, num)

    if result != None:
      print(f"Writing data - {result[1]} into main memory address - {result[0]}")
      self.main_memory.write(result[0], result[1])


  # register retrieval
  # right now it only puts the calculation answer in a special place that doesn't get cleaned
  def load_r(self, arg1):
    print(f"Reading from Register {arg1}")
    result = self.register.read(arg1)
    self.store_r('00111', result)

  # memory retrieval - (memory address, registration destination)
  def load_m(self, arg1, arg2):
    print(f"Reading from cache address - {arg1}")
    result = self.cache.read(arg1)
    print(f"cache read result ---> {result}")

    if result == None:
      print(f"Reading from main memory address - {arg1}")
      result = self.main_memory.read(arg1)
      self.cache.write(arg1, result)

    if result == None:
      print(f"address doesn't exist or no data is in address")
    else:
      self.register.write(result, arg2)


  # gets answer ready for printing
  def jump(self, arg1):
    print(f"Calculation result stored in output in order to be printed")
    self.output += ALU.remove_num_len(self.register.read(arg1))
    self.store_m('11110', arg1)
    if self.overflow == 1:
      arg2 = ALU.ADD_parser(arg1, '1')
      self.output = self.output + ' with overflow: ' + ALU.remove_num_len(self.register.read(arg2))
      self.store_m('11111', arg2)
      self.overflow = 0
      return
    

  # prints answer
  def show_output(self):
    print()
    print(f"Output: {self.function_identifier[self.function_index][0]} of {self.function_identifier[self.function_index][1]} and {self.function_identifier[self.function_index][2]} equals {self.output}")
    print()
    self.output = ''


  # ALU add function - (top num, bottom num, answer destination register)
  def alu_add(self, arg1, arg2, arg3):
    print(f"Adding {arg1} and {arg2}")

    arg1 = self.register.read(arg1)
    arg2 = self.register.read(arg2)
    self.alter_function(arg1, arg2)

    result = ALU.ADD_parser(arg1, arg2)
    print(f"Add result {result} stored in register {arg3}")
    self.register.write(result, arg3)

  # ALU subtraction function - (top num, bottom num, answer destination register)
  def alu_sub(self, arg1, arg2, arg3):
    print(f"Subtracting {arg2} from {arg1}")

    arg1 = self.register.read(arg1)
    arg2 = self.register.read(arg2)
    self.alter_function(arg1, arg2)

    result = ALU.SUB_parser(arg1, arg2)
    print(f"Subtraction result {result} stored in register {arg3}")
    self.register.write(result, arg3)

  # ALU multiplication function - (top num, bottom num, answer destination register)
  # overflow register (arg4) is created from destination register
  def alu_mult(self, arg1, arg2, arg3):
    print(f"Multiplying {arg1} and {arg2}")

    arg1 = self.register.read(arg1)
    arg2 = self.register.read(arg2)
    self.alter_function(arg1, arg2)

    result_hi, result_lo = ALU.MULT_parser(arg1, arg2)
    self.register.write(result_lo, arg3)
    if int(result_hi,2) != 0:
      self.overflow = 1
      arg4 = ALU.ADD_parser(arg3, '1')
      self.register.write(result_hi, arg4)
      print(f"Multiplication result_lo {result_lo} and result_hi {result_hi} stored in registers {arg3} and {arg4}")
      return

    print(f"Multiplication result_lo {result_lo} stored in register {arg3}")

  # ALU division function - (top num, bottom num, answer destination register)
  # overflow register (arg4) is created from destination register
  def alu_div(self, arg1, arg2, arg3):
    print(f"Dividing {arg1} with {arg2}")

    arg1 = self.register.read(arg1)
    arg2 = self.register.read(arg2)
    self.alter_function(arg1, arg2)

    result_lo, result_hi = ALU.DIV_parser(arg1, arg2)
    self.register.write(result_lo, arg3)
    if int(result_hi,2) != 0:
      self.overflow = 1
      arg4 = ALU.ADD_parser(arg3, '1')
      self.register.write(result_hi, arg4)
      print(f"Division result_lo {result_lo} and result_hi {result_hi} stored in registers {arg3} and {arg4}")
      return

    print(f"Multiplication result_lo {result_lo} stored in register {arg3}")



my_isa = ISA()
my_isa.instruction_reader('instructions.py')


