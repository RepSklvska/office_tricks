# 只能在Windows中运行
# doc在新目录存为docx，docx复制粘贴到新目录
def doc_to_docx(path_read, path_output):
	import os
	doc_files = []
	docx_files = []
	for root, dirs, files in os.walk(path_read):
		if len(files) != 0:
			for file in files:
				if file[-4:] == ".doc":
					doc_files.append(root.replace("\\", "/") + "/" + file)
	# 打开word批量将doc原地另存为docx
	from win32com import client as wc
	word = wc.Dispatch("Word.Application")
	for file in doc_files:
		doc = word.Documents.Open(file.replace("/", "\\"))
		doc.SaveAs(file + "x", 12)
		doc.Close()
	word.Quit()
	for root, dirs, files in os.walk(path_read):
		if len(files) != 0:
			for file in files:
				if file[-5:] == ".docx":
					docx_files.append(root.replace("\\", "/") + "/" + file)
	# docx复制粘贴到新目录
	import shutil
	for file in docx_files:
		shutil.copyfile(file, path_output + "/" + file.split("/")[-1])
	return
