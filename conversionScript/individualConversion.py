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

def convert_xml_to_csv(input_folder, output_folder):
    """
    Convert XML files in input_folder to CSV files in output_folder.
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each XML file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(input_folder, filename)
            csv_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.csv')

            # Parse XML
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            # Flatten XML structure
            flattened_data = flatten_xml(root)

            # Write flattened data to CSV
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.DictWriter(csvfile, fieldnames=flattened_data.keys())
                csv_writer.writeheader()
                csv_writer.writerow(flattened_data)

            print(f"Converted '{filename}' to '{os.path.basename(csv_file_path)}'")

# Example usage
input_folder = '/home/user1/Documents/XMLtoCSV/xmlFiles'
output_folder = '/home/user1/Documents/XMLtoCSV/csvFiles'
convert_xml_to_csv(input_folder, output_folder)

