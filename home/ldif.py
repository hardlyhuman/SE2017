from ldif3 import LDIFParser
from pprint import pprint

parser = LDIFParser(open('data.ldif', 'rb'))
i=0
for dn, Entry in parser.parse():
	if(i<3):
		i+=1
		continue
	dn.split(',')
	props=dict(item.split("=") for item in dn.split(","))
	#print('got entry record: %s' % dn)
	#print(props)
	#pprint(Entry)
	print (Entry["uid"],Entry["givenname"],Entry["sn"],Entry["mail"])
