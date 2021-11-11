
# gates

def gNAND(a,b):
  if a:
    if b:
      return 0
  return 1

def gNOT(a):
  if a:
    return 0
  return 1

def gAND(a,b):
  if a and b:
    return 1
  return 0

def gOR(a,b):
  if a and b:
    return 1
  if a or b:
    return 1
  return 0

def gXOR(a,b):
  if a:
    if b:
      return 0
    return 1

  if b:
    if a:
      return 0
    return 1

  return 0

def gGTZ(a):
  if int(a, 2) > 0:
    return 1
  return 0

def gLTZ(a):
  if int(a, 2) < 0:
    return 1
  return 0


# add

def half_adder(a,b):
  s = gXOR(a,b)
  c_out = gAND(a,b)
  return s,c_out

def half_adder2(s,c_in):
  s2 = gXOR(s,c_in)
  c2 = gAND(s,c_in)
  return s2,c2

def full_adder(a,b,c_in=0):
  s,c_out = half_adder(a,b)
  s2,c2 = half_adder2(s, c_in)
  c_in = gXOR(c_out,c2)
  return s2,c_in

def ADD_fork(a,b,c,opcode):
  if opcode == 0:
    s,c = half_adder(a,b)
  elif opcode == 1:
    s,c = full_adder(a,b,c)

  return s,c



# add parser uses the full adder or the half adder depending on the carry
def ADD_parser(num1, num2):
  c = None
  total_binary_num = ''  
  
  # adds zeros to even up the binary numbers
  num1, num2 = add_num_len(num1, num2)

  for i in range(len(num1)-1, -1, -1):

    # beginning - no carry
    if c == None:
      s,c = ADD_fork(int(num1[i]), int(num2[i]), 0, 0)

    # carry added
    else:
      s,c = ADD_fork(int(num1[i]), int(num2[i]), c, 1)
    total_binary_num = str(s) + total_binary_num
  
  # if the last number carried is a 1, it's added to the front. 0 is dropped.
  if c == 1:
    total_binary_num = str(c) + total_binary_num

  # returns total_binary_num - binary number in string form
  return total_binary_num



# subtract - uses the flip and add method

def SUB_parser(num1, num2):
  
  # adds zeros. evening out the numbers
  num1, num2 = add_num_len(num1, num2)

  # flips the lowest number using the "addition" subtraction method
  num2 = SUB_flip(num2)

  # adds 1 to the flip
  num2 = ADD_parser(num2, '1')

  # adds the two final numbers
  total = ADD_parser(num1, num2)

  # removes the first number from the binary result, leaving the answer
  total = total[1:]
  if int(total, 2) == 0:
    total = '0'
  else:
    total = remove_num_len(total)

  # returns total - binary number in string form
  return total

# uses the NOT gate to flip the bits
def SUB_flip(num):
  
  new_num = ''
  for i in range(len(num)):
    new_num += str(gNOT(int(num[i])))

  # returns the flipped binary number in string form
  return new_num



# multiply

# register is used to hold two numbers as a time
# one product at a time is added to the total.

def MULT_parser(num1, num2):
  total_binary_num = ''
  bin_shift = 0
  temp_reg = ['0','0']

  for i in range(len(num2)-1, -1, -1):
    total_binary_num = total_binary_num + bin_shift * '0'
    for j in range(len(num1)-1, -1, -1):
      total_binary_num = str(half_multiplier(int(num1[j]),int(num2[i]))) + total_binary_num
    bin_shift += 1

    if gNOT(gGTZ(temp_reg[0])):
      temp_reg[0] = total_binary_num
      total_binary_num = ''
      continue
    
    temp_reg[1] = total_binary_num
    temp_reg[0] = ADD_parser(temp_reg[0], temp_reg[1])

    total_binary_num = ''
    
  
  temp_reg[0], temp_reg[1] = add_num_len(temp_reg[0], None, 64)
  temp_reg[1] = '0'

  # returns binary numbers as strings - 64 bit separated into HI and LO registers
  return temp_reg[0][:32], temp_reg[0][32:]


def half_multiplier(a,b):
  return str(gAND(a,b))


# division

def DIV_parser(num1, num2, overflow=0):

  num1 = remove_num_len(num1)
  num2 = remove_num_len(num2)

  total_binary_num = ''
  temp_reg = ['0','0','0']
  overflow_num = ''
  overflow_index_start = len(num1)
  total_binary_num_count = 32
  position = 0
  second_time = 0

  num1 = add_num_len_end(num1, total_binary_num_count)

  temp_reg[0], temp_reg[1] = DIV_num_len(num1, num2)

  # makes sure the number doesn't go past 32 bits
  while total_binary_num_count > 0:

    temp_reg[0], temp_reg[1] = DIV_num_len(temp_reg[0], num2)

    temp_reg[0], part_binary_num, part_binary_num_count, sub_value_len = DIV_halfdiv(temp_reg[0], temp_reg[1], second_time)
    total_binary_num_count = total_binary_num_count - part_binary_num_count
    total_binary_num = total_binary_num + part_binary_num
    second_time = sub_value_len


  # separates the unsigned answer from the possible overflow (remainder)
  # like multiplication, it puts the two different parts into the HI (overflow) and LO (answer)
  
  temp_reg[1] = total_binary_num[overflow_index_start:]
  temp_reg[0] = total_binary_num[:overflow_index_start]

  temp_reg[0], temp_reg[2] = add_num_len(temp_reg[0], None, 32)
  temp_reg[1] = remove_num_len(temp_reg[1], 1, 1)
  temp_reg[1], temp_reg[2] = add_num_len(temp_reg[1], None, 32)

  # returns the answer and overflow in binary string form
  return temp_reg[0], temp_reg[1] 


# division has its own number lengthener
def DIV_num_len(num1, num2):

  if int(num2, 2) > int(num1, 2):
    zero_add = len(num2) - len(num1)
    zero_add += 1

    num1 = num1 + (zero_add * '0')

  return num1, num2


# looping division function
# loops until the divisor is the smaller number
# the remaining numbers are added onto the result and returned

def DIV_halfdiv(num1, num2, second_time=0):

  part_binary_num = ''
  part_binary_num_count = 0
  position = 0
  sub_value_len = 0

  if int(num1,2) == 0:
    return '0', '0', 1, 0

  for i in range(len(num1)):

    if int(num1[:i+1+second_time],2) < int(num2, 2):
      part_binary_num = part_binary_num + '0'
      part_binary_num_count += 1
      position += 1
      continue

    else:
      part_binary_num = part_binary_num + '1'
      part_binary_num_count += 1

      sub_value = SUB_parser(num1[:i+1+second_time], num2)
      sub_value_len = len(sub_value)
      return_value = sub_value + num1[i + 1 + second_time:]

      # returns the parts which are then added or subtracted from the wholes.
      return return_value, part_binary_num, part_binary_num_count, sub_value_len



# testing

def test_half_adder():
  for combo in [[0,0],[0,1],[1,0],[1,1]]:
    (sum, carry) = half_adder(combo[0], combo[1])
    print(str(combo) + "  " + "sum: " + str(sum) + " carry: " + str(carry))

def test_full_adder():
  for combo in [[0,0,0],[1,1,1],[0,1,1],[1,1,0]]:
    sum, carry = full_adder(combo[0], combo[1], combo[2])
    print(str(combo) + "  " + "sum: " + str(sum) + " carry: " + str(carry))

def test_ALU():
  for combo in [[0,0,0,0],[0,0,1,1],[1,1,1,0],[1,1,1,1]]:
    sum, carry = ALU(combo[0], combo[1], combo[2], combo[3])
    print(str(combo) + "  " + "sum: " + str(sum) + " carry: " + str(carry))


        
# functions that add or remove zeros from the numbers to achieve equal length or correct bit length

def add_num_len(num1, num2 = None, leng=32):

  if num2 == None:
    num2 = leng * '0'
    temp_len = leng - len(num1)
    for i in range(abs(temp_len)):
      num1 = '0' + num1


  for num in [num1, num2]:
    for i in num:
      if i not in ['0','1']:
        print('not binary')
        break

  dec_num1 = int(num1, 2)
  dec_num2 = int(num2, 2)

  if dec_num1 != dec_num2 or len(num1) != len(num2):
    if dec_num1 >= dec_num2:
      big_num, small_num = num1, num2
    else:
      big_num, small_num = num2, num1

    add_range = len(big_num) - len(small_num)
    for i in range(add_range):
      small_num = '0' + small_num

    return big_num, small_num

  return num1, num2

def remove_num_len(num, rem_front=1, rem_back=0):

  if rem_front == 1:
    
    if gNOT(int(num[0])) == 1:
      num = remove_num_len(num[1:], rem_front, rem_back)
  if rem_back == 1:
    
    if gNOT(int(num[-1])) == 1:
      num = remove_num_len(num[:-1], rem_front, rem_back)

  return num

def add_num_len_end(num, total_len):
  add_len = total_len - len(num)
  num = num + (add_len * '0')

  return num
  







# test_half_adder()
# test_full_adder()
# test_ALU()

mult_reg = {'HI': None, 'LO': None}
div_reg = {'HI': None, 'LO': None}

#print(f"ADD_answer ---> {ADD_parser('1101', '11100011110')}")
#print(SUB_flip('100011100'))
#print(f"SUB answer - {SUB_parser('10111', '101')}")

#print(f"remove_num_test --> {remove_num_len('000011001100')}")

#mult_reg['HI'], mult_reg['LO'] = MULT_parser('10001110111', '1001')
#print(f"multiply answer ---> regHI - {mult_reg['HI']}, regLO - {mult_reg['LO']}")
#print(f"final multiply answer ---> {remove_num_len(mult_reg['LO'])}")

#div_reg['LO'], div_reg['HI'] = DIV_parser('1011101', '10')
#print(f"division answer ---> regHI(overflow) - {div_reg['HI']}, regLO(answer) - {div_reg['LO']}")
#print(f"final division answer ---> {remove_num_len(div_reg['LO'], 1, 0)}")

#div_reg['LO'], div_reg['HI'] = DIV_parser('11110011', '100')
#print(f"division answer ---> regHI(overflow) - {div_reg['HI']}, regLO(answer) - {div_reg['LO']}")
#print(f"final division answer ---> {remove_num_len(div_reg['LO'], 1, 0)}")

#gate_test = [[0,0],[1,0],[0,1],[1,1]]

#for i in gate_test:
#  print(f"gNAND --> {gNAND(i[0], i[1])}")
#for i in gate_test:
#  print(f"gNOT --> {gNOT(i[0])}")
#for i in gate_test:
#  print(f"gAND --> {gAND(i[0], i[1])}")
#for i in gate_test:
#  print(f"gOR --> {gOR(i[0], i[1])}")
#for i in gate_test:
#  print(f"gXOR --> {gXOR(i[0], i[1])}")
  