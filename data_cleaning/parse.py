f = open("parse.csv")
t = open("new.csv", 'a')

new_data = []

for line in f:
	line = line.strip()
	new_data.append('L.' + line)

print new_data

for item in new_data:
	t.write(item+'\n')

f.close()
t.close()