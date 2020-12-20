def list_to_txt(filename, list_):
	# 仅适用于一维数组
	file = open(filename, 'w', encoding='UTF-8')
	for i in list_:
		file.write(i + '\n')
	file.close()
