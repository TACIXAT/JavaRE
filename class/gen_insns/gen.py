from bs4 import BeautifulSoup as BS
import re
import json

def clean(s):
	return re.sub(r'\s+', ' ', s.strip())

class Instruction:
	def __init__(self, insn):
		self.name = insn.select_one('h3 em').text
		self.description = clean(
			insn.select_one('div[title="Operation"] p.norm').text)
		self.mnemonic = [clean(ea.text) for ea in 
			insn.select('div[title="Format"] p > span.emphasis')]
		self.opcode = clean(insn.select_one('div[title="Forms"] p.norm').text)
		self.stack = [clean(ea.text) for ea in 
			insn.select('div[title="Operand Stack"] p.norm')]

	def print(self):
		print(self.name)
		print(self.description)
		print(self.mnemonic)
		print(self.opcode)
		print(self.stack)

	def json(self):
		return json.dumps({
			"name": self.name,
			"description": self.description,
			"mnemonic": self.mnemonic,
			"opcode": self.opcode,
			"stack": self.stack,
		}, indent=4, ensure_ascii=False)

with open('se7_insns.html', 'rb') as f:
	html = f.read()

soup = BS(html, 'html.parser')
insns = soup.select('.section-execution')
count = 0
for insn in insns[1:]:
	instruction = Instruction(insn)
	if len(instruction.mnemonic) == 1:
		count += 1
	else:
		print(instruction.json())
		print()

print('{} / {}'.format(count, len(insns[1:])))
