import os
import numpy as np

from AVL_Class import Aircraft_AVL 

if __name__ == '__main__':
	# Create instance of AVL aircraft
	x = Aircraft_AVL()

	# Choose where to save file
	dir_name = 'Results'
	x.AddFileInfo('Directory', dir_name)

	# Speicfy command to run AVL
	avl_cmd = 'avl'
	x.AddFileInfo('AVL_CMD', avl_cmd)
	
	# Geometry template file (and mass file if ncessary)
	# geo_template = 'Geo_File_Temp.avl'
	# x.AddFileInfo('Geometry_Template', geo_template)

	# Specify geometry file to use in AVL without modifying it
	geo_file = 'WingBody.avl'
	x.AddFileInfo('Geometry', geo_file)

	# Specify which variable to change in AVL (NOTE: make sure they are in array or list form)
	# Fying condition variables
	x.UpdateFlyingCond('AOA', np.linspace(1, 9, 9))
	# x.UpdateFlyingCond('Velocity', np.linspace(10, 20, 6))
	x.UpdateFlyingCond('Mach', [0.7, 0.85, 0.87])

	# Geometry Variables
	# x.UpdateGeometry('NChord_Wing', [5, 10, 150])
	# x.UpdateGeometry('NSpan_Wing', [25, 30, 35])
	# x.UpdateGeometry('NChord_HT', [5, 10, 15])
	# x.UpdateGeometry('NSpan_HT', [15, 20, 25])

	# Create directory if not exist yet
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)


	# x.PrintStoredVals()
	# x.Prepare_and_Run_AVL()
	x.RunAVLwithGeoFile()
	x.Read_File()
	