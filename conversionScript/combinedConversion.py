
import os
import csv
import xml.etree.ElementTree as ET

def flatten_xml(root, parent_path='', separator='.'):
    """
    Flatten XML structure into a dictionary.
    """
    result = {}
    path = parent_path + separator + root.tag if parent_path else root.tag

    # Add attributes as columns
    for attr, value in root.attrib.items():
        result[f"{path}.{attr}"] = value

    if len(root) == 0:
        result[path] = root.text
    else:
        for child in root:
            result.update(flatten_xml(child, path, separator))
    return result

def convert_xmls_to_csv(input_folder, output_file):
    """
    Convert XML files in input_folder to CSV files in output_file.
    """
    # Determine all possible field names by processing each XML file
    fieldnames = set()
    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(input_folder, filename)

            # Parse XML
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            # Flatten XML structure and update fieldnames
            flattened_data = flatten_xml(root)
            fieldnames.update(flattened_data.keys())

    # Process each XML file in the input folder
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
        csv_writer.writeheader()

        for filename in os.listdir(input_folder):
            if filename.endswith('.xml'):
                xml_file_path = os.path.join(input_folder, filename)

                # Parse XML
                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # Flatten XML structure
                flattened_data = flatten_xml(root)

                # Write flattened data to CSV
                csv_writer.writerow(flattened_data)

                print(f"Converted '{filename}' and appended to '{output_file}'")

# Example usage
input_folder = '/home/user1/Documents/XMLtoCSV/xmlFiles'  # Folder containing all XML files
output_file = '/home/user1/Documents/XMLtoCSV/csvFiles/combined_output.csv'

# Convert and append all XML files to a single CSV
convert_xmls_to_csv(input_folder, output_file)
