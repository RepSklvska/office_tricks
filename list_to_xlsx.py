def list_to_xlsx(filename, list_):
	import xlsxwriter
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet('Sheet')
	for i in range(0, len(list_)):
		worksheet.write_row(i, 0, list_[i])
	workbook.close()
