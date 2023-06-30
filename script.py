import os
import json
import subprocess
import shutil

# Directory where the files are located
directory = 'Sample_JSON_30May23'

# Request the input file name from the user
input_file_name = input("Enter the name of the input file (without .json extension): ")
input_file_path = os.path.join(directory, input_file_name + '.json')
try:
    with open(input_file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"File {input_file_path} not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error reading file {input_file_path}. Make sure it is a JSON file.")
    exit()

# Extracting the values of id from the bundledProductOffering array
bundled_product_offerings = data.get('productOffering', {}).get('bundledProductOffering', [])
updated_ids = []
for product in bundled_product_offerings:
    product_id = product.get('id', '')
    if product_id:
        # Searching for the corresponding file with a prefix in the Sample_JSON_30May23 directory
        found = False
        for file_name in os.listdir(directory):
            if product_id in file_name:
                prefix = file_name.split('_')[0]
                updated_ids.append(prefix + '_' + product_id)
                found = True
                break
        if not found:
            updated_ids.append('G_' + product_id)

# Looping through each file name from updated_ids
files_to_remove = []
for file_name in updated_ids:
    # Building file path
    file_path = os.path.join(directory, file_name + ".json")
    
    # Opening and loading JSON file
    try:
        with open(file_path, "r") as file:
            file_data = json.load(file)
            
            # Check if file has prefix R_ and process prodSpecCharValueUse
            if file_name.startswith("R_"):
                prod_spec_char_value_uses = file_data["productOffering"].get("prodSpecCharValueUse", [])
                for char_value_use in prod_spec_char_value_uses:
                    if char_value_use.get("name") == "promotion_soc":
                        product_spec_value = char_value_use.get("productSpecCharacteristicValue", "").strip()
                        if product_spec_value:
                            related_file_name = f"S_{product_spec_value}.json"
                            related_file_path = os.path.join(directory, related_file_name)
                            if os.path.exists(related_file_path):
                                updated_ids.append(related_file_name.split('.json')[0])
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        files_to_remove.append(file_name)
    except json.JSONDecodeError:
        print(f"Error reading file {file_path}.")

# Removing non-existent files from updated_ids.txt
updated_ids = [item for item in updated_ids if item not in files_to_remove]

# Writing the updated IDs to the updated_ids.txt file
with open('updated_ids.txt', 'w') as file:
    for updated_id in updated_ids:
        file.write(updated_id + '\n')

# Set to store unique productSpecification IDs with prefix
unique_product_spec_ids = set()

# Reading additional productSpecification from the specified file
try:
    with open(input_file_path, "r") as currentfile:
        current_file_data = json.load(currentfile)
        currentdata = current_file_data["productOffering"].get("productSpecification", [])
except FileNotFoundError:
    print(f"File {input_file_path} not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error reading file {input_file_path}. Make sure it is a JSON file.")
    exit()

# Looping through each file name from updated_ids
files_that_exist = set()
for file_name in updated_ids:
    # Building file path
    file_path = os.path.join(directory, file_name + ".json")

    # Opening and loading JSON file
    try:
        with open(file_path, "r") as file:
            file_data = json.load(file)

            # Getting the productSpecification array and adding additional data
            product_specifications = file_data["productOffering"].get("productSpecification", []) + currentdata

            # Adding each ID with 'FTR_' prefix to the set
            for product_spec in product_specifications:
                spec_id = product_spec.get("id", "")
                if spec_id:
                    unique_product_spec_ids.add("FTR_" + spec_id)
            files_that_exist.add(file_name.split('_')[-1])
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error reading file {file_path}.")

# Filter the bundledProductOffering array
new_bundled_product_offerings = [
    product for product in bundled_product_offerings if product.get('id') in files_that_exist
]

# Update the data
data['productOffering']['bundledProductOffering'] = new_bundled_product_offerings

# Create a copy of the original file
shutil.copy(input_file_path, os.path.join(directory, input_file_name + '_copy.json'))

# Save the modified data to the copy file
copy_file_path = os.path.join(input_file_name + '_copy.json')
with open(copy_file_path, 'w') as file:
    json.dump(data, file, indent=2)

# Writing unique productSpecification IDs to a new file
with open("product_spec_ids.txt", "w") as output_file:
    for spec_id in unique_product_spec_ids:
        output_file.write(spec_id + "\n")

# Running the final_output.py script as a subprocess
subprocess.run(["python", "final_output.py"])