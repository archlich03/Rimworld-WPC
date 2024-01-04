import re
import glob
import json

def extract_person_data(file_content, output_file):
    match = re.search(r'<first>(.*?)</first>.*?<last>(.*?)</last>.*?<skills>(.*?)</skills>', file_content, re.DOTALL)
    
    if match:
        name = match.group(1).strip()
        last_name = match.group(2).strip()
        skills_data = match.group(3).strip()

        person_data = {
            "Name": name,
            "Last Name": last_name,
            "Skills": []
        }

        skill_entries = re.findall(r'<li>(.*?)</li>', skills_data, re.DOTALL)
        for skill_entry in skill_entries:
            skill_name_match = re.search(r'<def>(.*?)</def>', skill_entry)
            skill_level_match = re.search(r'<level>(.*?)</level>', skill_entry)
            skill_passion_match = re.search(r'<passion>(.*?)</passion>', skill_entry)

            skill_name = skill_name_match.group(1) if skill_name_match else "Not specified"
            skill_level = skill_level_match.group(1) if skill_level_match else "-1"
            skill_passion = skill_passion_match.group(1) if skill_passion_match else "No"

            skill_data = {
                "SkillName": skill_name,
                "SkillLevel": skill_level,
                "SkillPassion": skill_passion
            }

            person_data["Skills"].append(skill_data)

        output_file.write(json.dumps(person_data, indent=2) + "\n")

input_files = glob.glob('*_output.txt')
output_file_path = 'skills.json'

with open(output_file_path, 'w') as output_file:
    for file_path in input_files:
        with open(file_path, 'r') as file:
            file_content = file.read()

        matches = re.finditer(r'START(.*?)NEXT', file_content, re.DOTALL)
        for match in matches:
            person_data = match.group(1).strip()
            extract_person_data(person_data, output_file)
