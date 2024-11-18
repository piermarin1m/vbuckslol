import json

def combine_json_files(file1, file2, output_file, unique_key="account_id"):
    # Load the data from both files
    with open(file1, "r", encoding="utf-8") as f1:
        data1 = json.load(f1)
    with open(file2, "r", encoding="utf-8") as f2:
        data2 = json.load(f2)

    # Use a dictionary to ensure unique entries based on unique_key
    combined_data = {item[unique_key]: item for item in data1}
    
    # Add items from the second file, avoiding duplicates
    for item in data2:
        if item[unique_key] not in combined_data:
            combined_data[item[unique_key]] = item

    # Convert dictionary values back to a list
    unique_combined_list = list(combined_data.values())

    # Write the unique combined list to the output file
    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(unique_combined_list, output, indent=4)

    print(f"Combined JSON saved to {output_file}")

# Example usage:
combine_json_files("/Users/drake/Downloads/gift-web/dbs/added_223ae36b0946495a8ac5ec63370c2810.json", "/Users/drake/Downloads/gift-web/dbs/added_b0fbe18932bb40469c5dc13e2d3f98ac.json", "combined_output.json")
