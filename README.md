# 地址

[http://10.100.73.17:8000/xpath](http://10.100.73.17:8000/xpath)

# 请求方式

- GET
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6cbf3984-39d1-4baf-be5d-0ad56c920258/Untitled.png)
    
- POST
    - 参数类型 JSON
    - html 网页源码
    - strings 需要生成 xpath 的字符串，支持多段中的文字
    - 样例
        
        ```json
        {
        	"html": "",
        	"strins": ""
        }
        ```
        

# 返回值

- 网页形式
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7587dbeb-b6fe-48c4-b25a-ac760af70f33/Untitled.png)
    
- 接口形式
    
    ```json
    {'code': 2, 'data': [{'shortest_xpath': '//p[@class="otitle"]/text()', 'longest_xpath': '/html[@id="ne_wrap"]/body/div[@class="container clearfix"]/div[@class="post_main"]/div[@class="post_content"]/div[@class="post_body"]/p[@class="otitle"]'}, {'shortest_xpath': '//h1[@class="post_title"]/text()', 'longest_xpath': '/html[@id="ne_wrap"]/body/div[@class="container clearfix"]/div[@class="post_main"]/h1[@class="post_title"]'}, {'shortest_xpath': '//html[@id="ne_wrap"]/head/title/text()', 'longest_xpath': '/html[@id="ne_wrap"]/head/title'}]}
    ```
    

# 生成流程

- 去掉查询字符串strings的空格换行，使用函数condition查找符合条件的tag（tag中的文本包含strings）
- 倒序循环结果，保留包含strings的最小tag
- 循环tag的所有父tag，判断是否有指定的属性known_attribute_list，有的话保存为`tag.name][key:value]`,否则为`tag.name`,判断该tag在同级别tag中是否唯一，不是的话加上对应的序号
- 使用 / 倒叙拼接，并验证是否为最短 xpath