file_path = 'output.txt'

with open(file_path, 'r') as file:
    # Read all lines and remove commas
    lines = [line.replace(',', '') for line in file.readlines()]

with open('output.txt', 'w') as cleaned_file:
    cleaned_file.writelines(lines)
