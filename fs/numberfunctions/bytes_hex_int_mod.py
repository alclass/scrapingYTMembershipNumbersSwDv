#!/usr/bin/python3
'''
sha1sum "2020-06-27 [UOL] advogada-assumi-erro-por-plagio-e-pede-desculpas-a-moro.htm"
   9e3b077ca945e6943a0d4c850715cc93f81a7972
 0x9e3b077ca945e6943a0d4c850715cc93f81a7972
'''
import copy

class BytesHexIntStaticConvertor:

  @staticmethod
  def from_hexstr_to_int(hexstr):
    return int(hexstr, 16)

  @staticmethod
  def from_int_to_hexstr(ii):
    return str(hex(ii))

  @staticmethod
  def from_hexstr_to_bytes(hexstr):
    return bytes(hexstr, encoding="'utf-8")

  @staticmethod
  def from_bytes_to_hexstr(p_bytes):
    return str(p_bytes, encoding="'utf-8")

  @staticmethod
  def from_binary_to_hex(p_binary):
    '''
      Not tested yet (the p_binary should be a 0's 1's data item, not exactly bytes)
    :return:
    '''
    return p_binary.hex()

  @classmethod
  def from_bytes_to_int(cls, p_bytes):
    h = cls.from_bytes_to_hexstr(p_bytes)
    return cls.from_hexstr_to_int(h)

  @classmethod
  def from_int_to_bytes(cls, ii):
    h = cls.from_int_to_hexstr(ii)
    return cls.from_hexstr_to_bytes(h)

class BytesHexIntConvertor:

  allowed_cycle_list_items = ['int', 'hexstr', 'bytes'] # binary as 0's & 1's is missing here, consider it a TO-DO

  def __init__(self, value, vtype=None, p_cycle_list=None):
    self.value = value
    self.current_vtype = vtype
    self.ordered_cycle_list = []
    self.cycle_pairs = []
    self.check_p_cycle_list(p_cycle_list)
    self.check_vtype()

  def check_p_cycle_list(self, p_cycle_list):
    if p_cycle_list is None or type(p_cycle_list) != list:
      self.cycle_list = copy.copy(self.allowed_cycle_list_items)
      return
    self.cycle_list = copy.copy(p_cycle_list)
    # there is a function to check item to item in package fs

  def check_vtype(self):
    raiseValueError = False
    if self.current_vtype == 'int':
      if not type(self.value) == int:
        raiseValueError = True
    if self.current_vtype == 'hexstr':
      if not type(self.value) == str:
        raiseValueError = True
    if self.current_vtype == 'bytes':
      if not type(self.value) == bytes:
        raiseValueError = True
    if raiseValueError:
      error_msg = 'Wrong type %s for %s' %(self.current_vtype, str(self.value))
      raise ValueError(error_msg)

  def mount_ordered_cycle_list(self, pos_idx):
    vtypes = copy.copy(self.cycle_list)
    vtype = vtypes[pos_idx]
    self.ordered_cycle_list = [vtype]
    del vtypes[pos_idx]
    self.ordered_cycle_list += vtypes

  def next_type(self, pos_idx):
    if pos_idx >= len(self.ordered_cycle_list):
      pos_idx = 0
    return self.ordered_cycle_list[pos_idx]

  def cycle(self):
    '''
      Cycles convertion of int, hexstr and bytes
    Obs:
      1) method cycle() takes three steps rolling within int, hexstr & bytes (in any order);
      2) because of random order, all combinations must be provisioned;
      3) altogether, there are A(3,2) = 3!/(3-2)! = 3x2=6, ie 6 if-cases; all of them methods in the static help class above (BytesHexIntStaticConvertor)
    :return:
    '''
    bhi = BytesHexIntStaticConvertor
    pos_idx = self.cycle_list.index(self.current_vtype)
    self.mount_ordered_cycle_list(pos_idx)
    for i, vtype in enumerate(self.ordered_cycle_list):
      # cycle_list = ['int', 'hexstr', 'bytes']  # binary as 0's & 1's is missing here, consider it a TO-DO
      next_vtype = self.next_type(i + 1)
      if vtype == 'int' and next_vtype == 'hexstr':
        forward_value = bhi.from_int_to_hexstr(self.value)
        self.cycle_pairs.append((self.value, forward_value))
        self.value = forward_value
      elif vtype == 'int' and next_vtype == 'bytes':
        forward_value = bhi.from_int_to_bytes(self.value)
        self.cycle_pairs.append((self.value, forward_value))
        self.value = forward_value
      elif vtype == 'hexstr' and next_vtype == 'bytes':
        forward_value = bhi.from_hexstr_to_bytes(self.value)
        self.cycle_pairs.append((self.value, forward_value))
        self.value = forward_value
      elif vtype == 'hexstr' and next_vtype == 'int':
        forward_value = bhi.from_hexstr_to_int(self.value)
        self.cycle_pairs.append((self.value, forward_value))
        self.value = forward_value
      elif vtype == 'bytes' and next_vtype == 'int':
        forward_value = bhi.from_bytes_to_int(self.value)
        self.cycle_pairs.append((self.value, forward_value))
        self.value = forward_value
      elif vtype == 'bytes' and self.next_type(i+1) == 'hexstr':
        forward_value = bhi.from_bytes_to_hexstr(self.value)
        self.cycle_pairs.append((self.value, forward_value))
        self.value = forward_value
      else:
        error_msg = 'Cycle tuple got into a non combinatorial pair %s <=> %s' %(vtype, self.next_type(i+1))
        raise ValueError(error_msg)

  def report(self):
    print ('BytesHexIntConvertor Report:')
    print ('Cycle ', self.ordered_cycle_list)
    for pair in self.cycle_pairs:
      print (pair)

def adhoc_test1():
  bhi = BytesHexIntStaticConvertor
  hex_str = '0xa'
  ii = bhi.from_hexstr_to_int(hex_str)
  print ('from_hexstr_to_int(hex_str=%s)' %hex_str, type(ii), ii)
  ret_hex_str = bhi.from_int_to_hexstr(ii)
  print ('from_int_to_hexstr(ii=%d)' %ii, type(ret_hex_str), ret_hex_str)
  ret_bytes = bhi.from_hexstr_to_bytes(ret_hex_str)
  print ('from_hexstr_to_bytes(hex_str=%s)' %ret_hex_str, type(ret_bytes), ret_bytes)
  ret_hex_str = bhi.from_bytes_to_hexstr(ret_bytes)
  print ('from_bytes_to_hexstr(ret_bytes=%s)' %ret_bytes, type(ret_hex_str), ret_hex_str)
  ii = bhi.from_bytes_to_int(ret_bytes)
  print ('from_bytes_to_int(ret_bytes=%s)' %ret_bytes, type(ii), ii)
  ret_bytes = bhi.from_int_to_bytes(ii)
  print ('from_int_to_bytes(ii=%d)' %ii, type(ret_bytes), ret_bytes)

def adhoc_test2():

  print('-'*50)
  bhi_o = BytesHexIntConvertor(value=10, vtype='int')
  bhi_o.cycle()
  bhi_o.report()

  print('-'*50)
  bhi_o = BytesHexIntConvertor(value=b'0xf1', vtype='bytes')
  bhi_o.cycle()
  bhi_o.report()

  print('-'*50)
  bhi_o = BytesHexIntConvertor(value=b'0xf1', vtype='bytes', p_cycle_list=['bytes', 'hexstr', 'int'])
  bhi_o.cycle()
  bhi_o.report()

def process():
  adhoc_test2()

if __name__ == '__main__':
  process()
