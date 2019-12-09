field_map = {}
with open('../results.txt', 'r') as file:
    for line in file:
        field = line.strip().split(':')[0]
        if field == '':
            continue
        if field_map.get(field, None) is not None:
            field_map[field] += 1
        else:
            field_map[field] = 1
count = 0
for key, value in field_map.items():
    if value > 10000:
        print(key.lower() + ': ' + str(value))
        count += 1
print("total attributes: " + str(count))
