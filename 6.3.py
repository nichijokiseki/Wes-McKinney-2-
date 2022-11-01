# 许多网站上有一些通过JSON或其他格式提供数据的公共API，通过Python访问的一个简单方法就是使用requests包
# 为了搜索最新的30个GitHub上的pandas主题，可以发起一个HTTP GET请求，使用requests扩展库
import pandas as pd
import requests
url = "https://api.github.com/repos/pandas-dev/pandas/issues"
resp = requests.get(url)
print(resp)
# 响应对象的方法json会返回一个包含被解析过的JSON字典，加载到Python对象当中
data = resp.json()
print(data[0]["title"])
# data中的每个元素都是一个包含所有GitHub主题页数据的字典
# 可以直接传递数据到DataFrame，并提取感兴趣的字段
issues = pd.DataFrame(data, columns=["number", "title", "labels", "state"])
pd.set_option("display.max_columns", None)
print(issues)
# 花费一些精力，就可以创建一些更高级的常见的Web API的接口，返回DataFrame对象进行分析