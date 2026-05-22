import random

qtd_points_per_class = 100 
file_name = 'data/2ddatabase.txt'

print(f"Generating {qtd_points_per_class * 2} points...")

with open(file_name, 'w') as file:
	for _ in range(qtd_points_per_class):
		x = round(random.uniform(0.0, 5.0), 2)
		y = round(random.uniform(0.0, 5.0), 2)
		file.write(f"{x},{y},0\n")

	for _ in range(qtd_points_per_class):
		x = round(random.uniform(5.1, 10.0), 2)
		y = round(random.uniform(5.1, 10.0), 2)
		file.write(f"{x},{y},1\n")

print(f"File '{file_name}' generated successfully!")