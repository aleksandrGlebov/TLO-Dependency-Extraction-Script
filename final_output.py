# Function to format a line from product_spec_ids.txt
def format_product_spec_id(spec_id):
    if spec_id.startswith("FTR_"):
        return f"\"gs://telus-kb-feature/test/{spec_id}.json\""
    return spec_id

# Function to format a line from updated_ids.txt
def format_updated_id(updated_id):
    if updated_id.startswith("O_"):
        return f"\"gs://telus-kb-add-ons/{updated_id}.json\""
    elif updated_id.startswith("R_"):
        return f"\"gs://telus-kb-add-ons/{updated_id}.json\""
    elif updated_id.startswith("G_"):
        return f"\"gs://telus-kb-add-ons/{updated_id}.json\""
    elif updated_id.startswith("S_"):
        return f"\"gs://telus-kb-add-ons/{updated_id}.json\""
    return updated_id

# Reading and formatting data from product_spec_ids.txt
formatted_product_spec_ids = []
try:
    with open("product_spec_ids.txt", "r") as file:
        for line in file:
            spec_id = line.strip()
            formatted_product_spec_ids.append(format_product_spec_id(spec_id))
except FileNotFoundError:
    print("File product_spec_ids.txt not found.")

# Reading and formatting data from updated_ids.txt
formatted_updated_ids = []
try:
    with open("updated_ids.txt", "r") as file:
        for line in file:
            updated_id = line.strip()
            formatted_updated_ids.append(format_updated_id(updated_id))
except FileNotFoundError:
    print("File updated_ids.txt not found.")

# Writing formatted data to a new file
with open("formatted_output.txt", "w") as output_file:
    all_formatted_lines = formatted_product_spec_ids + formatted_updated_ids
    for index, formatted_line in enumerate(all_formatted_lines):
        # Adding a comma to all lines except the last one
        if index < len(all_formatted_lines) - 1:
            output_file.write(formatted_line + ",\n")
        else:
            output_file.write(formatted_line + "\n")