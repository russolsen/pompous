# -*- coding: utf-8 -*-

from parser import Parser
from bytecode import Label, Instr, Bytecode
import marshal
import importlib.util

class Instruction:
  def __init__(self, opcode, arg=None, label=None):
    self.opcode = opcode
    self.arg = arg
    self.label = label

  def __repr__(self):
    result = self.opcode
    if self.label:
      result = self.label + " " + result
    if self.arg:
      result = result + " " + str(self.arg)
    return result

class Assembler:
  def __init__(self, f):
    self.labels = dict()
    self.parsed= []
    self.instructions = []
    self.assemble(f)

  def _assem_line(self, line):
    #print("line:", line)
    p = Parser(line)

    if p.opcode == None:
      return

    if p.label:
      self.instructions.append(self._label_for_id(p.label))

    if p.arg:
      self.instructions.append(Instr(p.opcode, self._parse_arg(p.arg)))
    else:
      #print("opcode:", p.opcode)
      self.instructions.append(Instr(p.opcode))

  def _parse_arg(self, arg):
    #print("parse arg", arg, self._is_label(arg))
    if not arg:
      return arg
    if self._is_label(arg):
      #print("arg is label", arg)
      return self._label_for_id(arg)
    #print(arg)
    return eval(arg)

  def _is_label(self, s):
    #print("is lab:", s)
    return s[-1] == ':' or s[0] == ':'

  def _strip_colons(self, s):
    if s[0] == ':':
      s = s[1:]
    if s[-1] == ':':
      s = s[:-1]
    return s

  def _label_for_id(self, s):
    lid = self._strip_colons(s)
    if not self.labels.get(lid):
      self.labels[lid] = Label()
    return self.labels[lid]

  def assemble(self, f):
    lines = f.readlines()
    for line in lines:
      self._assem_line(line)
    self.bytecodes = Bytecode(self.instructions)
    self.code = self.bytecodes.to_code()
