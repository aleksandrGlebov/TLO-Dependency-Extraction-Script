# TLO Dependency Extraction Script

This script is designed to automate the process of extracting dependencies from TLO (Top Level Offering) JSON files and outputting them in a formatted manner.

## 📝 How the Script Works

1. 🖥️ The script **prompts the user** to enter the name of the input file (without the `.json` extension). This file should be located in a directory, which is named 'Sample_JSON_30May23' by default, but the user can change the directory's name and the script will still function properly.

2. 📂 The script **opens and reads** the content of the specified JSON file. If the file is not found or contains invalid JSON, the script reports an error and exits.

3. 🔍 It **extracts the `id` values** from the `bundledProductOffering` array within the file and looks for corresponding files in the directory with prefixes (e.g., `O_`, `R_`, `G_`, `S_`). The prefix is taken from the filename in the directory that contains the identifier.

4. 🔄 For each identifier found, the script **checks for a file** with the corresponding prefix and identifier in the same directory, opens it, and processes its content. If the file's prefix is `R_`, the script also checks for `promotion_soc` values and adds additional dependencies.

5. 📝 All identifiers found are **written to a file** named `updated_ids.txt`.

6. ✨ The script also **extracts unique identifiers** from `productSpecification` and writes them to a file named `product_spec_ids.txt` with the prefix `FTR_`.

7. 📋 A **copy of the original input file** is created with the suffix `_copy`.

8. 💾 The modified data is **saved to this copy file**. The original file remains untouched.

9. 🚀 The script **executes `final_output.py`** as a subprocess, which reads data from `product_spec_ids.txt` and `updated_ids.txt`, formats them, and writes to a new file named `formatted_output.txt`.

10. 🧹 The script **executes `remove_temp_files.py`** as a subprocess, which deletes temporary files `product_spec_ids.txt` and `updated_ids.txt`.

## 📌 Notes

- Please ensure that the script is in the **same directory** as the `Sample_JSON_30May23` folder or the folder you are using.
- The **original input file is not modified** by the script; all changes are made to a copy of the file.

## 🔧 Requirements

- Python 3.x

## 🚀 Usage

Execute the script by running:

```shell
python <script.py>
```
