import requests
from lxml import etree
import os
import re
# url = "http://image4.it168.com/2010/1/7/6da7296e-4052-4cca-9a70-5620f92bd5fe.jpg"
#
# r = requests.get(url)
# with open("1.jpg","wb") as f:
#     f.write(r.content)

# os._exit(0)
def bingImg(word):
    # 1、拿到url
    url = "https://cn.bing.com/images/async?q="+word+"&first=" \
          "36&count=35&relp=35&scenario=ImageBasicHover&datsrc=N_I&layout=RowBa" \
          "sed&mmasync=1"

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) Apple'
                             'WebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3'
                             '626.121 Safari/537.36'}
    # 2、拿到前段代码
    r = requests.get(url,headers=headers)
    ret = r.text#获取url里面的前端代码，字符串数据类型

    # 3、拿到所有图片url
    #需要转换ret为可以应用的格式re，lxml（xpath），ba4，pyquery
    result = etree.HTML(ret)#ret字符串对象变为XML的对象
    content_list = result.xpath('//a[@class="iusc"]/@m')#content_list保存了连接
    #将图pain路径从连接中提取出来
    print(len(content_list))
    # os._exit(1)
    for content in content_list:
        img = re.search('"murl":"(.*?)","',content).group(1)
        print(img)
        # 4、保存图片
        # r = requests.get(img)
        try:
            r = requests.get(img,headers=headers,timeout=10)
        except:
            print(img,"图片无法下载")
            continue
        name = img[-10:]#去url的后十位作为图片的名字
        name = re.sub("/","",name)#re.sub作用是利用正则表达式去实现相对复杂的字符串的替换处理
        with open(word+"/" + name,"wb") as f:
            f.write(r.content)#r.content是图片的二进制数据内容
        # os._exit(0)

if __name__=="__main__":
    word = input("请输入你想下载的图片：")
    if not os.path.exists(word+"/"):
        os.mkdir(word+"/")
    bingImg(word)
