#!/usr/bin/python3
import fs.numberfunctions.bytes_hex_int_mod as bhimod
import unittest

# BHI_stat = bhimod.BytesHexIntStaticConvertor # static class
BHI_inst = bhimod.BytesHexIntConvertor # instantiable class

class TestCase(unittest.TestCase):

  def test_1(self):
    '''

    :return:
    '''
    expected_int = 241
    bhi_o = BHI_inst(value=expected_int, vtype='int')
    bhi_o.cycle()
    returned_int = bhi_o.get_int()
    self.assertEqual(expected_int, returned_int)

    expected_bytes = b'0xf1'
    returned_bytes = bhi_o.get_bytes()
    self.assertEqual(expected_bytes, returned_bytes)

    expected_hexstr = '0xf1'
    returned_hexstr = bhi_o.get_hexstr()
    self.assertEqual(expected_hexstr, returned_hexstr)

    expected_int = 10
    bhi_o = BHI_inst(value=expected_int, vtype='int')
    bhi_o.cycle()
    returned_int = bhi_o.get_int()
    self.assertEqual(expected_int, returned_int)

    expected_bytes = b'0xa'
    returned_bytes = bhi_o.get_bytes()
    self.assertEqual(expected_bytes, returned_bytes)

    expected_hexstr = '0xa'
    returned_hexstr = bhi_o.get_hexstr()
    self.assertEqual(expected_hexstr, returned_hexstr)

def process():
  pass

if __name__ == '__main__':
  process()