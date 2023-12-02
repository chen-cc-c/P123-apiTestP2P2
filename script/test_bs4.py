from bs4 import BeautifulSoup

html="""
<html>
<head><title>黑马程序员</title></head>
<body>
<p id="test01">软件测试</p>
<p id="test02">2020年</p>
<a href="/api.html">接口测试</a>
<a href="/web.html">Web自动化测试</a>
<a href="/app.html">APP自动化测试</a>
</body>
</html>
"""

soup=BeautifulSoup(html,'html.parser')
print(soup.title)# 获取title标签
print(soup.title.name) # 获取title标签的名称
print(soup.title.string) # 获取title标签的文本内容
print(soup.p) # 获取第一个p标签
print(soup.p["id"]) # 获取第一个p标签的id属性值
print(soup.find_all("a")) # 获取所有的a标签
# 获取所有的a标签，并遍历打印a标签的href属性值和文本内容
for s in soup.find_all('a'):
    print("hrdf={} text={}".format(s['href'],s.string))