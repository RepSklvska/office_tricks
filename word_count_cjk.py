# 统计出和Word一样的中文字符和朝鲜语单词数值
def word_count_cjk(string):
	import re
	cjk_words = re.sub(r"[^(\u4e00-\u9fa5，。《》？；’‘：“”【】、）（…￥！·)]", "", string)
	# print("中文字符和朝鲜语单词", len(cjk_words))
	count = len(cjk_words)
	return count
