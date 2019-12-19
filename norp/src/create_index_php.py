import os

python_url = os.environ['python_url']
file = open('/src/index_template.php','r').read()
output = file.replace('PYTHON_URL', python_url)
output_file = open("/src/index.php", 'w')
output_file.write(output)

file = open('/src/reorderUpdate_template.php', 'r').read()
output = file.replace('PYTHON_URL', python_url)
output_file = open("/src/reorderUpdate.php", 'w')
output_file.write(output)

file = open('/src/elo_template.php', 'r').read()
output = file.replace('PYTHON_URL', python_url)
output_file = open("/src/elo.php", 'w')
output_file.write(output)