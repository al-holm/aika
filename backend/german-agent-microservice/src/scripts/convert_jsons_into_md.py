import json
import os
from pathlib import Path

def transform_json_to_markdown(input_filepath, output_filepath):
    # Read the JSON file
    with open(input_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Write the data to a markdown file
    with open(output_filepath, 'w', encoding='utf-8') as file:
        def write_dict(d, indent=0):
            for key, value in d.items():
                if isinstance(value, dict):
                    file.write(f"{'#' * (indent // 4 + 1)} {key}\n\n")
                    write_dict(value, indent + 4)
                elif isinstance(value, list):
                    file.write(f"{'#' * (indent // 4 + 1)} {key}\n\n")
                    for item in value:
                        if isinstance(item, dict):
                            write_dict(item, indent + 4)
                        else:
                            file.write(f"{' ' * indent}- \n {item}\n")
                    file.write('\n')
                else:
                    file.write(f"{'#' * (indent // 4 + 1)} {key}: \n {value}\n")
            file.write('\n')

        write_dict(data)

def process_files(input_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for input_filepath in Path(input_directory).glob('*.json'):
        output_filepath = Path(output_directory) / (input_filepath.stem + '.md')
        transform_json_to_markdown(input_filepath, output_filepath)
        print(f"Processed {input_filepath} -> {output_filepath}")

if __name__ == "__main__":
    input_dir = "C:/Users/tommc/OneDrive/Dokumente/progs/nest/aika/backend/german-agent-microservice/src/out"
    output_dir = "C:/Users/tommc/OneDrive/Dokumente/progs/nest/aika/backend/german-agent-microservice/src/out/converted_jsons"
    process_files(input_dir, output_dir)