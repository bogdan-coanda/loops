class Measures(object):
			
	DM = 32
	RH = 8

	xydelta = {}

	xydelta[8] = [
		(0, DM*(8-2)*(8-1)), 
		(DM*((8-3)*(8-2)-1), 0), 
		(DM*(8-1), 0), 
		(0, DM*8), 
		(DM, 0), 
		(0, DM), 
		(0, 0)]				
		
	xydelta[7] = [
		(DM*((7-3)*(7-2)-1), 0), 
		(DM*(7-1), 0), 
		(0, DM*7), 
		(DM, 0), 
		(0, DM), 
		(0, 0)]
		
	xydelta[6] = [
		(0, DM*6), 
		(DM*(6-1), 0), 
		(DM, 0), 
		(0, DM), 
		(0, 0)]
		
	xydelta[5] = [
		(DM*(6-1), 0), 
		(DM, 0), 
		(0, DM), 
		(0, 0)]				
		
	xydelta[4] = [
		(DM, 0), 
		(0, DM), 
		(0, 0)]				
		
if __name__ == "__main__":
	
	print(Measures.xydelta[8])
