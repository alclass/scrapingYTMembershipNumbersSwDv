#!/usr/bin/python3
import re

regexp_str = r'\[(.+)\]'
compiled_re = re.compile(regexp_str)

entry = '2020-05-24 Clayson Fi [cUCWE75Qq5ExU0qlwQSkx18wQ] '
match_obj = compiled_re.search(entry)
if match_obj:
  print (match_obj.group(1))
else:
  print ('match was None')


