import os
import numpy as np

from AVL_Class import Aircraft_AVL 

if __name__ == '__main__':
	# Create instance of AVL aircraft
	x = Aircraft_AVL()

	# Choose where to save file
	dir_name = 'Test'
	x.AddFileInfo('Directory', dir_name)

	# Speicfy command to run AVL
	avl_cmd = '/home/kharad/Code/avl'
	x.AddFileInfo('AVL_CMD', avl_cmd)
	
	# Geometry file (and mass file if ncessary)
	geo_template = 'Geo_File_Temp.avl'
	x.AddFileInfo('Geometry', geo_template)

	# Specify which variable to change in AVL (NOTE: make sure they are in array or list form)
	# Fying condition variables
	x.UpdateFlyingCond('AOA', np.linspace(-2, 2, 5))
	# x.UpdateFlyingCond('Velocity', np.linspace(10, 20, 6))
	# x.UpdateFlyingCond('Mach', np.linspace(0, 0.9, 10))

	# Geometry Variables
	x.UpdateGeometry('NChord_Wing', [5, 10, 15])
	# x.UpdateGeometry('NSpan_Wing', [25, 30, 35])
	# x.UpdateGeometry('NChord_HT', [5, 10, 15])
	# x.UpdateGeometry('NSpan_HT', [15, 20, 25])

	# Create directory if not exist yet
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)


	x.PrintStoredVals()
	x.Prepare_and_Run_AVL()
	x.Read_File()
	