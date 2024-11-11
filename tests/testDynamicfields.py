from dataclasses import dataclass

from requests import Request

# 实例化 Request 对象
request = Request(method='GET', url='https://example.com')

# 动态添加字段
request.new_field = 'custom_value'

# 验证新字段
print(request.new_field)  # 输出: custom_value