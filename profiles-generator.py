import os
from dotenv import load_dotenv
load_dotenv()

# Define the variables
variables = {}
keys = ['CREDENTIAL_PATH_FOR_DBT', 'GCP_PROJECT_ID', 'DBT_PROJECT_NAME', 'DBT_DATASET_NAME']
for key in keys:
    variables[key] = os.environ.get(key)
    if variables[key]:
        print(f'Value for {key} is exist!')
    else:
        print(f'Value for {key} is not exist!')

# Read the template file
with open('template-profiles.yml', 'r') as file:
    template = file.read()

# Replace the variables in the template
for key, value in variables.items():
    print(key, value)
    template = template.replace("{{"+key+"}}", value)

# Ensure the ~/.dbt directory exists
dbt_dir = os.path.expanduser('~/.dbt')
os.makedirs(dbt_dir, exist_ok=True)

# Write the result to ~/.dbt/profiles.yml
with open(os.path.join(dbt_dir, 'profiles.yml'), 'w') as file:
    file.write(template)

print("profiles.yml has been generated successfully!")
