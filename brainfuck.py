from colorama import *
from collections import deque
import sys
from msvcrt import getch
from os.path import exists
init(convert=True)
print(Style.BRIGHT)
def error(msg):
	print(Fore.RED+msg)
	sys.exit(0)
try:
	bf_file=sys.argv[1]
	if bf_file[-3:]!='.bf':error('File should have extension .bf')
	elif not exists(bf_file):error('File not found')
except IndexError:
	error('No script provided')
with open(bf_file,'r') as script:
	bf=script.read()
#pair brackets
br1={}
br2={}
loops=deque()
for i,c in enumerate(bf):
	if c=='[':
		loops.append(i)
	elif c==']':
		pair=loops.pop()
		br1[pair]=i
		br2[i]=pair
#interpret
pointer=0
end=len(bf)
cells=[0]
items=1
c=0
while c!=end:
	cell_val=cells[pointer]
	exec(
		{
			'+':'''
cells[pointer]=cell_val+1
''',
			'-':'''
cells[pointer]=cell_val-1 if cell_val!=0 else 255''',
			'.':'''
print(chr(cell_val),end='')
''',
			',':'''
cells[pointer]=ord(getch().decode('utf-8'))
''',
			'<':'''
if pointer==1:
	cells.insert(0,0)
	items+=1
else:
	pointer-=1
''',
			'>':'''
if pointer==items-1:
	cells.append(0)
	items+=1
pointer+=1
''',
			'#':'''
try:
	number=int(bf[c+1])
except ValueError:
	error('# must be followed by a number')	
print('|')
for i in range(c-number,c+number+1):
	try:
		print(cells[i],end='|')
	except IndexError:
		continue
print('pointer at : '+str(pointer))
''',
			'[':'''
if cell_val==0:
	c=br1[c]
''',
			']':'''
if cell_val!=0:
	c=br2[c]
''',
		}.get(bf[c],'')
	)
	c+=1