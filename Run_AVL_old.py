import os
import numpy as np
import platform
import csv
import subprocess as sb

# Run AVL with command file specified as run_file
def Run_AVL_Command(run_file):
	avl_cmd = '/home/kharad/Code/avl'
	os.system(avl_cmd + ' < ' + run_file)
	# p = sb.Popen([avl_cmd, run_file])
	# p.wait()

# Create geometry file based on template
def Create_Geo_File(file_dict, geo_dict):
	temp_file = file_dict['Geo_Temp']
	new_file = file_dict['Geometry']

	with open(temp_file, 'r') as file:
		filedata = file.read()

	# Update geometry file values
	filedata = filedata.replace('NCHORD_W', str(geo_dict['Nchord_W']))
	filedata = filedata.replace('NSPAN_W', str(geo_dict['Nspan_W']))

	with open(new_file, 'w') as file:
		file.write(filedata)

# Create AVL command file with input/output files and flying conditions
def Create_Run_File(file_dict, geo_dict, cond_dict, run_num):
	with open(file_dict['Run'], 'w') as fid:

		# Load AVL geometry file
		fid.write('load %s\n' % file_dict['Geometry'])

		# Load AVL mass file if necessary
		if file_dict['Mass']:
			print('Mass file not empty\n')
			fid.write('mass %s\nmset 0\n' % file_dict['Mass'])

		# Enter OPER menu
		fid.write('oper\n')

		# Define run case conditions
		for vel in cond_dict['Velocity']:
			fid.write('m\n')
			fid.write('v %0.8f\n\n' % vel)

			for alpha in cond_dict['AOA']:
				fid.write('a a %0.8f\n' % alpha)

				# Run and save data to file
				fe_file = file_dict['FE_File'] + str(run_num[0]) + '.fe'
				fid.write('x\n')
				fid.write('fe\n%s\n' % fe_file)

				# Remove fe file before running AVL
				try:
					os.remove(fe_file)
				except OSError:
					pass

				# Write info of run case setup
				str_file = [str(run_num[0]), str(geo_dict['Nchord_W']), str(geo_dict['Nspan_W']), str(alpha), str(vel)]
				file_dict['Run_Info'].writerow(str_file)
				run_num[0] = run_num[0] + 1

		# Exist OPER menu
		fid.write('\n\n\n')

		# End AVL
		fid.write('quit\n')

# Read Force Element output file from AVL and save (x,y,z) and cp values to txt
def Read_File(fe_file):
	x = []; y = []; z = []; cp = []
	cd_data = fe_file[:-3] + '.csv'
	with open(cd_data, 'w') as fout:
		writer = csv.writer(fout, delimiter=',')
		writer.writerow(['X', 'Y', 'Z', 'dCp'])

		with open(fe_file, 'r') as fin:
			for content in fin:
				temp = content.split()
				if temp and (Check_Num(temp[0]) or temp[0] == '***'):
					x = float(temp[1])
					y = float(temp[2])
					z = float(temp[3])
					cp = float(temp[6])
					writer.writerow(['%0.8f' % x, '%0.8f' % y, '%0.8f' % z, '%0.8f' % cp])


# Check if string is a number
def Check_Num(input_str):
	try:
		float(input_str)
		return True
	except ValueError:
		return False

# Loop through different flight condition/Geometry setups and run AVL to get data
def Run_AVL_File(dir_name):

	# Need to specify below variables {
	# Geometry file (and mass file if ncessary)
	geo_file = 'Geo_File.avl'
	geo_template = 'Geo_File_Temp.avl'

	# mass_file = 'Example_Mass_File.mass'
	mass_file = []

	# Condition Variables
	AOA = np.linspace(-2, 2, 5)
	Velocity = np.linspace(10, 20, 11)
	Mach = np.linspace(0, 0.9, 10)

	# Geometry Variables
	NC_WING = [10]
	NS_WING = [30]
	# }

	# Create file to run avl command
	run_file = dir_name + '/Temp.run'
	run_info = dir_name + '/Run_Info.csv'
	run_num = [1]

	with open(run_info, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(['Run #', 'Nchord Wing', 'Nspan Wing', 'AOA', 'Velocity'])

		for NCW in NC_WING:
			for NSW in NS_WING:
				fe_file = dir_name + '/FE_run_'
				file_dict = {'Run': run_file, 'Geo_Temp': geo_template, 'Geometry': geo_file, 'Mass': mass_file, 'FE_File': fe_file, 'Run_Info': writer}
				geo_dict = {'Nchord_W': NCW, 'Nspan_W': NSW}
				cond_dict = {'AOA': AOA, 'Velocity': Velocity}

				Create_Geo_File(file_dict, geo_dict)
				Create_Run_File(file_dict, geo_dict, cond_dict, run_num)

				# Run AVL with input run file
				Run_AVL_Command(run_file)

	print("# of cases = %d" % run_num[0])
	# Extract necessary data from AVL file to text file
	for iter_num in range(1, run_num[0]):
		Read_File(dir_name + '/FE_run_' + str(iter_num) + '.fe')


if __name__ == '__main__':
	
	# Create directory if not exist yet
	dir_name = 'Test'
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)

	Run_AVL_File(dir_name)
	