import os
import sys
import numpy as np
import csv

class Aircraft_AVL:

	def __init__(self):

		# Flying condition
		self.__alpha = [0]
		self.__Mach = [0]
		self.__Vel = [12]

		# Geometry setup
		self.__NC_W = [10]
		self.__NS_W = [30]
		self.__NC_HT = [10]
		self.__NS_HT = [20]

		# Number of run cases
		self.__num_run = 1

		# Initialize file names
		self.__dir_name = []
		
		self.__geo_file = 'Geo_File.avl'
		self.__mass_file = []

		# Get template file for geometry
		self.__geo_temp = []

		# Specify AVL command
		self.__avl_cmd = []

	# Update flight condition for AVL
	def UpdateFlyingCond(self, key, val):
		if key == 'AOA':
			self.__alpha = val
		elif key == 'Mach':
			self.__Mach = val
		elif key == 'Velocity':
			self.__Vel = val
		else:
			sys.exit('UpdateFlyingCond: %s option not found!' % key)

		self.__num_run = self.__num_run * len(val)

	# Update number of panels in AVL geo file
	def UpdateGeometry(self, key, val):
		if key == 'NChord_Wing':
			self.__NC_W = val
		elif key == 'NSpan_Wing':
			self.__NS_W = val
		elif key == 'NChord_HT':
			self.__NC_HT = val
		elif key == 'NSpan_HT':
			self.__NS_HT = val
		else:
			sys.exit('UpdateGeometry: %s option not found!' % key)

		self.__num_run = self.__num_run * len(val)

	# Add where to save file or which files to use for AVL
	def AddFileInfo(self, key, val):
		if key == 'Directory':
			self.__dir_name = val
			self.__run_file = val + '/AVL_Run_Case.run'
			self.__run_info = val + '/Run_Info.csv'
			self.__fe_file = val + '/FE_run_'
		elif key == 'Geometry':
			self.__geo_temp = val
		elif key == 'Mass':
			self.__mass_file = val
		elif key == 'AVL_CMD':
			self.__avl_cmd = val
		else:
			sys.exit('AddFileInfo: %s option not found!' % key)

	# Print out currently stored values
	def PrintStoredVals(self):
		print("Storing Directory: %s" % self.__dir_name)
		print("Run File: %s" % self.__run_file)
		print("Run Info: %s" % self.__run_info)
		print("Geometry File Template: %s" % self.__geo_temp)
		print("Mass File: %s\n" % self.__mass_file)

		print("AVL command: %s\n" % self.__avl_cmd)

		print("Angle of Attack: " + ', '.join(str(x) for x in self.__alpha))
		print("Mach #: " + ', '.join(str(x) for x in self.__Mach))
		print("Velocity: " + ', '.join(str(x) for x in self.__Vel) + '\n')

		print("NChord for Wing: " + ', '.join(str(x) for x in self.__NC_W))
		print("NSpan for Wing: " + ', '.join(str(x) for x in self.__NS_W))
		print("NChord for HorTail: " + ', '.join(str(x) for x in self.__NC_HT))
		print("NSpa for HorTail: " + ', '.join(str(x) for x in self.__NS_HT) + '\n')

		print("Number of cases to run: %d\n" % self.__num_run)

	# Create geometry files and run AVL
	def Prepare_and_Run_AVL(self):
		# Check if directory, avl cmd or geometry file is specified
		try:
			self.__dir_name[0]
			self.__avl_cmd[0]
			self.__geo_temp[0]
		except IndexError:
			sys.exit("Please specify directory/AVL command/template geometry file!!!")

		# Open file to store conditions for different run cases
		with open(self.__run_info, 'w') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
			writer.writerow(['Run #', 'Nchord Wing', 'Nspan Wing', 'Nchord HT', 'Nspan HT', 'Velocity', 'Mach', 'AOA'])

			self.Loop_AVL_Geometry(writer)

	# Loop through different geometry
	def Loop_AVL_Geometry(self, writer):
		run_num = [1]
		for NC_W in self.__NC_W:
			for NS_W in self.__NS_W:
				for NC_HT in self.__NC_HT:
					for NS_HT in self.__NS_HT:
						geo_dict = {'Nchord_W': NC_W, 'Nspan_W': NS_W, 'Nchord_HT': NC_HT, 'Nspan_HT': NS_HT}
						out_str = [str(NC_W), str(NS_W), str(NC_HT), str(NS_HT)]

						self.Create_Geo_File(geo_dict)
						self.Loop_AVL_FlyingCond(writer, run_num, out_str)
						self.Run_AVL()

	# Update geometry file based on input template file
	def Create_Geo_File(self, geo_dict):
		with open(self.__geo_temp, 'r') as file:
			filedata = file.read()

		# Update geometry file values
		filedata = filedata.replace('NCHORD_W', str(geo_dict['Nchord_W']))
		filedata = filedata.replace('NSPAN_W', str(geo_dict['Nspan_W']))
		filedata = filedata.replace('NCHORD_HT', str(geo_dict['Nchord_HT']))
		filedata = filedata.replace('NSPAN_HT', str(geo_dict['Nspan_HT']))

		with open(self.__geo_file, 'w') as file:
			file.write(filedata)

	# Loop through different fight conditions
	def Loop_AVL_FlyingCond(self, writer, run_num, out_str):
		with open(self.__run_file, 'w') as fid:

			# Load AVL geometry file
			fid.write('load %s\n' % self.__geo_file)

			# Load AVL mass file if necessary
			if self.__mass_file:
				fid.write('mass %s\nmset 0\n' % self.__mass_file)

			# Enter OPER menu
			fid.write('oper\n')

			# Define run case conditions
			for vel in self.__Vel:
				for mach in self.__Mach:
					fid.write('m\n')
					fid.write('v %0.8f\nmn %0.8f\n\n' % (vel, mach))

					for alpha in self.__alpha:
						fid.write('a a %0.8f\n' % alpha)

						# Run and save data to file
						fe_file = self.__fe_file + str(run_num[0]) + '.fe'
						fid.write('x\n')
						fid.write('fe\n%s\n' % fe_file)

						# Remove fe file before running AVL
						try:
							os.remove(fe_file)
						except OSError:
							pass

						# Write info of run case setup
						str_file = [str(run_num[0])] + out_str + [str(vel), str(mach), str(alpha)]
						writer.writerow(str_file)
						run_num[0] = run_num[0] + 1
					
			# Exist OPER menu
			fid.write('\n\n\n')

			# End AVL
			fid.write('quit\n')

	# Run AVL with command file specified in run_file
	def Run_AVL(self):
		os.system(self.__avl_cmd + ' < ' + self.__run_file)

	# Read Force Element output file from AVL and save (x,y,z) and cp values to txt
	def Read_File(self):
		# Check if string is a number
		def Check_Num(input_str):
			try:
				float(input_str)
				return True
			except ValueError:
				return False

		# Loop through fe files
		for run in range(1, self.__num_run + 1):
			x = []; y = []; z = []; cp = []
			cd_data = self.__fe_file + str(run) + '.csv'

			with open(cd_data, 'w') as fout:
				writer = csv.writer(fout, delimiter=',', lineterminator = '\n')
				writer.writerow(['X', 'Y', 'Z', 'dCp'])

				with open(self.__fe_file + str(run) + '.fe', 'r') as fin:
					for content in fin:
						temp = content.split()
						if temp and (Check_Num(temp[0]) or temp[0] == '***'):
							x = float(temp[1])
							y = float(temp[2])
							z = float(temp[3])
							cp = float(temp[6])
							writer.writerow(['%0.8f' % x, '%0.8f' % y, '%0.8f' % z, '%0.8f' % cp])
