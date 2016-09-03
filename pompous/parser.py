# -*- coding: utf-8 -*-

from shlex import shlex
from bytecode import Label, Instr, Bytecode
from collections import deque
from io import StringIO

class Parser:
  def __init__(self, line):
    self.label = None
    self.opcode = None
    self.arg = None
    lex = shlex(StringIO(line))
    lex.wordchars += ':'
    self.tokens = deque(list(lex))
    self.parse()

  def peek(self):
    if len(self.tokens) > 0:
      return self.tokens[0]
    else:
      return None

  def shift(self):
    if len(self.tokens) > 0:
      return self.tokens.popleft()
    else:
      return None

  def is_label(self, tok):
    return tok[0] == ':' or tok[-1] == ':'

  def parse(self):
    tok = self.shift()
    if not tok:
      return

    if self.is_label(tok):
      self.label = tok
      tok = self.shift()

    self.opcode = tok.upper()

    self.arg = " ".join(self.tokens)
    if self.arg == '':
      self.arg = None

#lp = LineParser("label:")
#print(lp.label)
#print(lp.op)
#print(lp.arg)
