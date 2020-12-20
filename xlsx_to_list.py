def xlsx_to_list(filename):
	import pandas
	origin_frame = pandas.read_excel(filename)
	columns = origin_frame.columns.to_list()
	list_from_xlsx = [columns]
	for i in origin_frame.index:
		line = []
		for ii in origin_frame.loc[i].values.tolist():
			line.append(str(ii).strip())
		list_from_xlsx.append(line)
	return list_from_xlsx
