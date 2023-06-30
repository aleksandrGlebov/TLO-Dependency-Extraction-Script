import os

# List of files to be removed
files_to_remove = ['product_spec_ids.txt', 'updated_ids.txt']

# Removing files from the list
for file_name in files_to_remove:
    try:
        os.remove(file_name)
        print(f"File {file_name} successfully removed.")
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except OSError as e:
        print(f"Error deleting file {file_name}: {e}")