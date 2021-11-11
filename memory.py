import alu_nocomments as ALU

class Memory():
  def __init__(self):
    self.name = 'Memory'
    self.blocks = {}
    self.current_block = None
    self.last_block = None


  # shifts the block to be written
  def block_shift(self):

    self.last_block = self.current_block

    if self.current_block == '00101':
      self.current_block = '00000'
      return

    self.current_block = ALU.ADD_parser(self.current_block, '00001')

  
  # checks length of value, all values must be 32 bits; a 64 bit value must be split
  def check_value_length(self, arg1):
    print(f"check_value_length ---> {arg1}")
    if len(arg1) != 32:
      print(f"value must be 32 bits in length.")
      return False

    return True


class Cache(Memory):

  # acts kind of like a hashmap - blocks have a [identifier tag, value]
  # current block and last block are used. cycling through the blocks anytime anything is stored.
  def __init__(self):
    self.name = 'Cache'
    self.blocks = {'00000': [None, None], '00001': [None, None], '00010': [None, None], '00011': [None, None], '00100': [None, None], '00101': [None, None]}
    self.current_block = '00000'
    self.last_block = '00000'

  # checks the blocks for the necessary tag
  # returns the value if tag is found, otherwise None is returned
  def check_blocks(self, arg1):
    for key in self.blocks.keys():
      if arg1 == self.blocks[key][0]:
        return self.blocks[key][1]

    return None
  

  # if the tag wasn't found, it will add or overwrite the [tag,value] of the current block
  # it will then shift the current block to the next available block
  # (address, data)
  def write(self, arg1, arg2):

    return_to_main_memory = None
    value = self.check_blocks(arg1)

    if not self.check_value_length(arg2):
      return

    print(f"Writing to Cache: {arg1} = {arg2}")
    if value != None:
      print(f"Cache - HIT")
    else:
      print(f"Cache - MISS")

    if self.blocks[self.current_block][0] != None:
      return_to_main_memory = [self.blocks[self.current_block][0], self.blocks[self.current_block][1]]
      
    self.blocks[self.current_block] = [arg1, arg2]

    self.block_shift()
    return return_to_main_memory



  # checks the blocks and returns a value if there is one
  def read(self, arg1):
    value = self.check_blocks(arg1)

    if value == None:
      print(f"Reading from Cache: MISS")
      return None

    print(f"Reading from Cache: HIT")
    return value




class Main_Memory(Memory):

  # Main memory has stored information - cache starts out with none, I'll have values stored in main memory
  # blocks as soon as I get the opcodes written
  def __init__(self):
    self.name = 'Main Memory'
    self.blocks = {'00000': None, '00001': None, '00010': None, '00011': None, '00100': None, '00101': None, '00110': None, '00111': None, '01000': None, '01001':None, '01010': None, '01011': None, '11110': None, '11111': None}
    self.current_block = '00000'
    self.last_block = '00000'
  

  # if the tag wasn't found, it will add or overwrite the [tag,value] if the current block
  # it will then shift the current block to the next available block
  def write(self, arg1, arg2):
    if self.check_value_length(arg2):
      print(f"Writing to Main Memory: {arg2} ")

      self.blocks[arg1] = arg2

    return

  # checks the blocks and returns a value if there is one
  def read(self, arg1):
    value = self.blocks[arg1]

    if value == None:
      print(f"Reading from Main_Memory: value not found")
      return None

    print(f"Reading from Main_Memory: returning value {value}")
    return value



