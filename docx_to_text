# 获得docx文件中的纯文本内容
def docx_to_text(filename):
	import re
	import zipfile
	file = zipfile.ZipFile(filename)
	content = file.read("word/document.xml").decode("utf-8")
	cleaned = re.sub(r"<(.|\n)*?>", "", content)
	return cleaned
