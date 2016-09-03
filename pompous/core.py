# -*- coding: utf-8 -*-

import marshal
import importlib.util
import sys
import os
from assembler import Assembler

MAGIC_NUMBER = importlib.util.MAGIC_NUMBER

def w_long(x):
  return (int(x) & 0xFFFFFFFF).to_bytes(4, 'little')

def code_to_bytecode(code, mtime=0, source_size=0):
  #data = bytearray(MAGIC_NUMBER)
  data = bytearray([0x3, 0xf3, 0xd, 0xa])
  data = bytearray([0x16, 0xd, 0xd, 0xa])
  data.extend(w_long(mtime))
  data.extend(w_long(source_size))
  data.extend(marshal.dumps(code))
  return data

def file_info(path):
  mtime = os.path.getmtime(path)
  size = os.path.getsize(path)
  return mtime, size

def path_to_pyc(path):
  components = os.path.splitext(path)
  return components[0] + ".pyc"

def file_to_code(path):
  with open(path) as f:
    a = Assembler(f)
    return a.code

def assemble(path):
  code = file_to_code(path)
  mtime, size = file_info(path)

  with open(path_to_pyc(path), 'wb') as f:
    f.write(code_to_bytecode(code, mtime, size))

def run(path):
  code = file_to_code(path)
  eval(code)

def main(argv):
  cmd = argv[0]
  paths = argv[1:]

  print(cmd)

  if cmd == 'run':
    for p in paths:
      run(p)
  elif cmd == 'assemble':
    for p in paths:
      assemble(p)
  else:
    print(cmd, '?')

if __name__ == "__main__":
  main(sys.argv[1:])
