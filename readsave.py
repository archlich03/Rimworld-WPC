import re
import glob

def extract_pawn_skills(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        faction_checked = False
        in_first_pawn_data = False
        in_pawn_entry = False
        inside_skills = False
        faction = None

        for line in input_file:
            if '<firstPawnData>' in line:
                in_first_pawn_data = True
            elif in_first_pawn_data and not faction_checked:
                if '<faction>' in line:
                    faction = re.search(r'<faction>(.*?)</faction>', line).group(1)
                    faction_checked = True
                    in_first_pawn_data = False
            if '<thing Class="Pawn">' in line:
                in_pawn_entry = True
            elif in_pawn_entry:
                if '<faction>' in line:
                    if re.search(r'<faction>(.*?)</faction>', line).group(1) != faction:
                        in_pawn_entry = False
                if '<first>' in line:
                    output_file.write("START\n")
                    output_file.write(line)
                if '<last>' in line:
                    output_file.write(line)
                if '<skills>' in line:
                    inside_skills = True
                    output_file.write(line)
                elif inside_skills:
                    output_file.write(line)
                    if '</skills>' in line:
                        inside_skills = False
                        in_pawn_entry = False
                        output_file.write("NEXT\n")
        output_file.write("END\n")

input_files = glob.glob('*.rws')

for input_file_path in input_files:
    output_file_path = input_file_path.replace('.rws', '_output.txt')
    
    extract_pawn_skills(input_file_path, output_file_path)
