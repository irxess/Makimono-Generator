import os

def rename_files_in_folder_to_lower_case(directory_path):
	if not os.path.isdir(directory_path):
		raise NotADirectoryError(f'To make sure all files in directory have lowe case names path to valid directory has to be supplied. Got {directory_path}, which does not seem to be an existing directory on your system.')

	files = os.listdir(directory_path)
	print('files', files)

	for file_name in files:
		# print('Now working on file:', file)
		path_to_current_file = os.path.join(directory_path, file_name)
		if os.path.isfile(path_to_current_file):
			# print('Is file =D', file)
			if file_name != file_name.casefold():
				path_to_new_file_name = os.path.join(directory_path, file_name.casefold())
				print(f'Renaming {path_to_current_file} to {path_to_new_file_name}')
				os.rename(path_to_current_file, path_to_new_file_name)

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-dir',
		'--directoryPath',
		help='(Optional) Path to the directory you want to lowercase the name of all the files in. If not set, the current working directory is called instead.')
	args = parser.parse_args()

	directory_path = ""
	if(args.directoryPath is not None):
		directory_path = args.directoryPath
	else:
		directory_path = os.getcwd()

	rename_files_in_folder_to_lower_case(directory_path)
