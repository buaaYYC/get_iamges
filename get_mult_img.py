from lxml import etree
import os
import re
import requests
#简易的多批次下载（爬虫）bing图片
"""
https://cn.bing.com/images/async?q=阿达是+&first=36&count=35&relp=35&scenario=ImageBasicHover&datsrc=N_I&layout=RowBased&mmasync=1
https://cn.bing.com/images/async?q=阿达是+&first=73&count=35&relp=35&scenario=ImageBasicHover&datsrc=N_I&layout=RowBased&mmasync=1
"""
#不断更新地址，相当于浏览网页时的翻页
def url_upgrade(word,num_url):
    url = "https://cn.bing.com/images/async?q=" + word + "&first=" \
          + str(num_url) + "&count=35&relp=35&scenario=ImageBasicHover&datsrc=N_I&layout=RowBa" \
                      "sed&mmasync=1"
    return  url
###############

def download_picture(num_page,word):
    """

    :param num_page: 需要下载多少页图片
    :return:
    """
    for i in range(num_page):
        url = url_upgrade(word,i*35)
        print("___")
        print(url)
        try:
            r = requests.get(url)
        except:
            print("无效链接")
            continue
        ret = r.text#获取url里面的前端代码，字符串数据类型
        result = etree.HTML(ret)#ret字符串对象变为XML的对象
        content_list = result.xpath('//a[@class="iusc"]/@m')#content_list保存了连接
        #将图pain路径从连接中提取出来
        print(len(content_list))
        #保存图片
        for content in content_list:
            img = re.search('"murl":"(.*?)","',content).group(1)
            print(img)
            # 4、保存图片
            # r = requests.get(img)
            try:
                r = requests.get(img,timeout=10)
            except:
                print(img,"图片无法下载")
                continue
            name = img[-10:]#去url的后十位作为图片的名字
            name = re.sub("/","",name)#re.sub作用是利用正则表达式去实现相对复杂的字符串的替换处理
            file_name = word + "/"
            with open(file_name + name,"wb") as f:
                f.write(r.content)#r.content是图片的二进制数据内容
    print("下载完成")

if __name__=="__main__":
    word = input("请输入想要下载的图片名：")
    file_name = word+"/"
    if not os.path.exists(file_name):
        os.mkdir(file_name)
    download_picture(1,word)