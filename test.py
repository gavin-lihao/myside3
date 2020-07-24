teas_list = [{'tea_id': 1, 'tea_name': 't李皓', 'class_name': '一年级3班'},
             {'tea_id': 1, 'tea_name': 't李皓', 'class_name': '一年级2班'},
             {'tea_id': 1, 'tea_name': 't李皓', 'class_name': '五年级1班'},
             {'tea_id': 2, 'tea_name': 't郭梦瑶', 'class_name': '一年级3班'},
             {'tea_id': 2, 'tea_name': 't郭梦瑶', 'class_name': '一年级2班'},
             {'tea_id': 3, 'tea_name': 'tlihao', 'class_name': '一年级2班'},
             {'tea_id': 3, 'tea_name': 'tlihao', 'class_name': '五年级1班'},
             {'tea_id': 4, 'tea_name': 'tgavin', 'class_name': '一年级3班'}
             ]

result = {}

for row in teas_list:
    tea_id = row['tea_id']
    if tea_id in result:
        result[tea_id]['class_name'].append(row['class_name'])
    else:
        result[tea_id] = {'tea_id': row['tea_id'], 'tea_name': row['tea_name'], 'class_name': [row['class_name'],]}

for item in result.values():
    print(item)
