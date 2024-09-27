import os
import patoolib

def extract_recursively(src_directory, output_directory):
    """
    Recursively extract archives from a directory and its subdirectories.
    """
    for entry in os.listdir(src_directory):
        full_entry_path = os.path.join(src_directory, entry)
        entry_output_directory = output_directory

        if os.path.isdir(full_entry_path):
            # If the entry is a directory, recurse into it
            nested_output_directory = os.path.join(output_directory, entry)
            print(f"Descending into directory: {full_entry_path}")
            extract_recursively(full_entry_path, nested_output_directory)
        elif os.path.isfile(full_entry_path):
            # Determine the output directory for extraction
            file_base_name = os.path.splitext(entry)[0]
            archive_output_directory = os.path.join(output_directory, file_base_name)
            if not os.path.exists(archive_output_directory):
                os.makedirs(archive_output_directory)
            # If the entry is a file, attempt to extract it
            print(f"Extracting {entry} into {archive_output_directory}")
            try:
                patoolib.extract_archive(full_entry_path, outdir=archive_output_directory)
            except Exception as e:
                print(f"Failed to extract {entry}. Reason: {e}")
        else:
            print(f"{entry} is neither a valid file nor directory, skipping...")

# Path to the directory containing files and directories you want to extract
directory = '/home/kog/repos/self-hosting/data-project/Cit0day.in_special_for_xss.is'
base_output_directory = os.path.join(directory, 'extracted')

# Ensure the base output directory exists
if not os.path.exists(base_output_directory):
    os.makedirs(base_output_directory)

# Start the recursive extraction
extract_recursively(directory, base_output_directory)

print("Recursive extraction complete for all applicable files and directories.")
