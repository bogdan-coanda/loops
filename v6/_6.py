from diagram import *
from uicanvas import *
from extension_result import *
from common import *
import itertools


def extend(addr):
	loop = diagram.nodeByAddress[addr].loop
	return diagram.extendLoop(loop)
	

if __name__ == "__main__":
	
	diagram = Diagram(6, 0)	
		
	print(diagram.cycles[0].py)

	# @0
	#extend('00004') #  green |  3,  -2-,  1
	#extend('00014') # violet |  1,  -4-, 12
	#extend('00024') #    red | 12, -13-, 16
	#extend('00034') # orange | 16,  -8-,  9
	#extend('00044') # yellow |  9,  -6-,  3

	# @5
	#extend('01104') #  green |  4,  -7-,  6
	#extend('01114') # orange |  6, -22-, 13
	#extend('01124') # violet | 13, -14-,  2
	#extend('01134') # yellow |  2, -11-,  8
	#extend('01144') #    red |  8, -20-,  4
	
	# @23	
	#extend('12304') #  green | 22, -21-, 20
	#extend('12314') # yellow | 20, -17-, 14
	#extend('12324') # orange | 14, -15-,  7
	#extend('12334') #    red |  7, -10-, 11
	#extend('12344') # violet | 11, -19-, 22
		
	# @18
	#extend('11204') #  green | 17, -16-, 19
	#extend('11214') #    red | 19,  -3-, 15
	#extend('11224') # yellow | 15, -12-, 21
	#extend('11234') # violet | 21,  -9-, 10
	#extend('11244') # orange | 10,  -1-, 17

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                 #
	
	# 8 » 7 | yellow | _4_, _1_, -7-, -10-
	# extend('00120')
	# extend('01030')
	# extend('01300')
	# extend('02210')

	# 7 » 6 | orange | _1_, -10-, +18+, -17-
	# extend('00110')
	# extend('02220')
	# extend('11100')
	# extend('11230')

	# 6 » 5	|    red | _1_, _2_, -17-, -14-
	# extend('00100')
	# extend('00230')
	# extend('10220') 
	# extend('11110')
	
	
	# 13 » 12 | purple | _2_, -14-, =13=, -5-
	# extend('00220')
	# extend('01110')
	# extend('10100')
	# extend('10230')	
			
	# 12 » 11 | yellow | _2_, -5-, =8=, -11-
	# extend('00210')
	# extend('01120')
	# extend('02030')
	# extend('02300')	
	
	
	# 19 » 18 | orange | _2_, _3_, -11-, -19-
	# extend('00330')
	# extend('00200')
	# extend('02310')
	# extend('11320')	
	
	# 18 » 17 |    red | _3_, -19-, +18+, -15-
	# extend('00320')
	# extend('10310')
	# extend('11200')
	# extend('11330')	

	# 17 » 16 | purple | _3_, _6_, -15-, -7-
	# extend('00310')
	# extend('01200')
	# extend('01330')
	# extend('10320')	

	# 30 » 34 |  green | _6_, -7-, =4=, -5-
	# extend('01240')
	# extend('01040')
	# extend('01140')
	# extend('01340')		

	# 34 » 33 | orange | _6_, -5-, =13=, -22-
	# extend('01230')
	# extend('01100')
	# extend('10110')
	# extend('12220')		

	# 33 » 32 |    red | _6_, _9_, -22-, -21-
	# extend('01220')
	# extend('02110')
	# extend('12100')
	# extend('12230')			

	# 46 » 45 | purple | _9_, -21-, -18-, -10-
	# extend('02100')
	# extend('02230')
	# extend('11220')
	# extend('12110')			

	# 40 » 44 |  green | _9_, _8_, -10-, -11-
	# extend('02040')
	# extend('02140')
	# extend('02240')
	# extend('02340')

	# 44 » 43 | yellow | _8_, -11-, =2=, -5-
	# extend('02030')
	# extend('00210')
	# extend('01120')
	# extend('02300')
	
	# 43 » 42 |    red | _8_, -5-, =4=, -20-
	# extend('02020')
	# extend('01000')
	# extend('01130')
	# extend('12010')
		
	# 42 » 41 | purple | _8_, _16_, -20-, -17-
	# extend('02010')
	# extend('11000')
	# extend('11130')
	# extend('12020')

	# 80 » 84 |  green | _16_, -17-, -18-, -19-
	# extend('11040')
	# extend('11140')
	# extend('11240')
	# extend('11340')

	# 68 » 67 |  green | _16_, _13_, -19-, -22-
	# extend('10120')
	# extend('11030')
	# extend('11300')
	# extend('12210')

	# 67 » 66 | orange | _13_, -22-, =6=, -5-
	# extend('10110')
	# extend('01100')
	# extend('01230')
	# extend('12220')

	# 66 » 65 | purple | _13_, -5-, =2=, -14-
	# extend('10100')
	# extend('00220')
	# extend('01110')
	# extend('10230')

	# 65 » 69 |  green | _13_, _12_, -14-, -15-
	# extend('10140')
	# extend('10040')
	# extend('10240')
	# extend('10340')
	
	# 64 » 63 | yellow | _12_, -15-, -18-, -21-
	# extend('10030')
	# extend('10300')
	# extend('11210')
	# extend('12120')
	
	# 22 » 21 | orange | _12_, _4_, -21-, -20-
	# extend('01010')
	# extend('10020')
	# extend('12000')
	# extend('12130')

	# 21 » 20 |    red | _4_, -20-, =8=, -5-
	# extend('01000')
	# extend('01130')
	# extend('02020')
	# extend('12010')

	# 20 » 24 |  green | _4_, -5-, =6=, -7-
	# extend('01040')
	# extend('01100')
	# extend('01240')
	# extend('01340')
							
	show(diagram)
	
