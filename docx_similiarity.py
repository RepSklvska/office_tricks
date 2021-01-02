# Must run in Python version >= 3.6
# 统计一个文件夹里面的docx文件之间的相似度（文件夹里必须全都是docx文件！），然后在上一级目录中生成一个xlsx文件

import os

import jieba
from gensim import corpora, models, similarities


def docx_to_text(filename):
	import re
	import zipfile
	try:
		file = zipfile.ZipFile(filename)
		content = file.read("word/document.xml").decode("utf-8")
		cleaned = re.sub(r"<(.|\n)*?>", "", content)
		# print(cleaned)
		return cleaned
	except zipfile.BadZipFile:
		return ""


def list_to_xlsx(filename, list_):
	import xlsxwriter
	workbook = xlsxwriter.Workbook(filename)
	worksheet = workbook.add_worksheet('Sheet')
	for i in range(0, len(list_)):
		worksheet.write_row(i, 0, list_[i])
	workbook.close()


path = r"/run/media/aa/TOSHIBA/统计相似度/XYZ"
dir_name = path.split("/")[-1]
os.chdir(path)

# cuts存放纯文本化的docx文件断句后生成的字符串列表
print("读取文件……", end="")
cuts = {}
for file in os.listdir():
	data = jieba.cut(docx_to_text(file))
	connected_with_space = ""
	for word in data:
		connected_with_space += word + " "
	cut = connected_with_space.split()
	cuts[file] = cut
print("完成")

# 此处参考教程，texts是把所有词汇列在了一个二维列表里
print("简单处理内容(1/5)：列出所有词汇")
documents = []
for file in cuts:
	data = ""
	for item in cuts[file]:
		data += item + " "
	documents.append(data)
texts = [[word for word in document.split()] for document in documents]

# 构建频率字典
print("简单处理内容(2/3)：构建频率词典")
from collections import defaultdict

frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1

# 过滤低频词汇
texts = [[word for word in text if frequency[token] > 3] for text in texts]

# 通过语料库建立词典
print("简单处理内容(3/3)：建立语料库词典")
dictionary = corpora.Dictionary(texts)
# dictionary.save()

# sims是每个文件的相似度统计
sims = {}
num = 1
for file in cuts:
	print("\r逐个比对文件内容(" + str(num) + "/" + str(len(cuts)) + ")", end="")
	num += 1
	# 把要对比的文档转为为稀疏向量
	vec = dictionary.doc2bow(cuts[file])
	# 对稀疏向量进行处理得到新语料库
	corpus = [dictionary.doc2bow(text) for text in texts]
	# 将新语料库通过TF-IDF模型处理得到TF-IDF值
	tfidf = models.TfidfModel(corpus)
	# 得到特征数
	feature_num = len(dictionary.token2id.keys())
	# 计算稀疏矩阵的相似度从而建立一个索引
	index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_num)
	# 最终相似度结果
	sim = index[tfidf[vec]]
	sims[file] = sim

#
line1 = [""]
for file in cuts:
	line1.append(file)

sheet = [line1]
for file in sims:
	line = [file]
	for i in sims[file]:
		line.append(i)
	sheet.append(line)

os.chdir("..")
list_to_xlsx(dir_name + " 相似度统计结果.xlsx", sheet)
