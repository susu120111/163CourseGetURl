import re
from urllib import request
import os
import sys
import shutil
all_course_url=[]

def get_page(url_any):
    """获取文本网页内容"""
    req=request.urlopen(url_any)
    content=req.read().decode("gb18030")
    return content


def get_all_course(url_any):
    """获取所有课程"""
    ss=get_page(url_any)
    sec_content=ss.split("var _movies = []")
    cc=re.compile(r"http://open.163.com/movie/[\d\/\w]{5,}\.html")
    global all_course_url
    tmp=cc.findall(sec_content[1])
    for x in tmp:
        if x not in all_course_url:
            all_course_url.append(x)
    print("\n获取到 {0} 个课程视频地址".format(len(all_course_url)))

def parse_html(course_url):
    """解析单个网页 获取视频名称等内容"""
    ss=get_page(course_url)
    tmp=ss.split("number : ")
    course_seq=int(tmp[1][:tmp[1].find(",")])
    tmp=tmp[1].split("title : '")
    vedio_name=tmp[1][:tmp[1].find("'")]
    course_name=tmp[2][:tmp[2].find("'")]
    if not os.path.exists(course_name):
        os.mkdir(course_name)
        f=open("dir.txt","a")
        f.write(course_name)
        f.close()
    tmp=tmp[1].split("appsrc : '")
    tmp=tmp[1][:tmp[1].find(".m3u8",0,90)]
    tmp=tmp.replace("mp4","flv")
    if tmp.find("-list")!=-1:
        inlist=tmp.find("-list")
        vedio_url=tmp[:-5]+".flv"
    elif  tmp.find("_shd")!=-1:
        vedio_url=tmp+".flv"
    else:
        vedio_url=tmp+".flv"
    name1="{0}.{1}".format(course_seq,vedio_name)
    print(name1+"\n")
    spUrl=vedio_url.split("/")
    spUrl=spUrl[9]
    vedio_url="\n"+vedio_url
    #下载地址写入地址文件
    f=open("URL.txt","a")
    f.write(vedio_url)
    f.close()
    #改名命令写入改名脚本文件
    f=open("rename.bat","a")
    f.write("rename "+spUrl+" "+name1+".flv\n")
    f.close()

if __name__=="__main__":
    #获取所有课程
    url=input("\n请打开课程内任一视频播放页面，复制其网址后粘贴并按回车键开始下载：\n")
    get_all_course(url)
    #生成地址文件和改名脚本文件，空文件
    f=open("URL.txt","w")
    f.close()
    f=open("rename.bat","w")
    f.close()
    f=open("dir.txt","w")
    f.close()
    #逐一下载课程
    for course in all_course_url:
        #获取视频下载链接
        vedio_url=parse_html(course)
    #打开辅助文件，获取文件夹名
    f=open("dir.txt","r")
    cp=f.read()
    f.close()
    #移动文件并删除辅助文件
    shutil.move("URL.txt",cp+"\\URL.txt")
    shutil.move("rename.bat",cp+"\\rename.bat")
    os.remove("dir.txt")
    input("课程地址信息获取完毕，请使用下载软件下载！完成后使用rename.bat更改文件名.")
