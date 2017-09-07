__author__='SHP'
#coding=utf-8
import urllib
import urllib2
import re
import thread
import time

#糗事百科爬虫类
class QSBK:
    def __init__(self):
        self.pageIndex=1
        self.user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
        self.headers={'User-Agent':self.user_agent}
        #存放段子的变量,每一个元素是每一页的段子
        self.stories=[]
        self.enable=False
    #传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url='http://www.qiushibaike.com/hot/page/'+str(pageIndex)
            request=urllib2.Request(url,headers=self.headers)
            response=urllib2.urlopen(request)
            #print response.read()
            pageCode=response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接服务器失败,错误原因:",e.reason
                return None
    #传入某一页代码,返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode=self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败"
            return None
        pattern=re.compile('<div class="author clearfix">.*?<img src=.*?alt="(.*?)">.*?<div class="content">.*?<span>(.*?)</span>.*?<!--.*?-->(.*?)<div class="stats">.*?<i.*?number">(.*?)</i>.*?<i.*?number">(.*?)</i>',re.S)
        items=re.findall(pattern,pageCode)
        #存储每页的段子
        pageStories=[]
        for item in items:
            haveImg=re.search("img",item[2])
            if not haveImg:
                replaceBR=re.compile('<br/>')
                text=re.sub(replaceBR,"\n",item[1])
                #item[0]表示发布者,item[1]表示内容,item[2]表示图片信息,item[3]表示点赞数,item[4]表示评论数
                pageStories.append([item[0].strip(),text.strip(),item[3].strip(),item[4].strip()])
        return pageStories
    #加载并提取页面的内容,加入到列表
    def loadPage(self):
        #如果当前未看的页数少于2页,则加载下一页
        if self.enable==True:
            if len(self.stories)<2:
                pageStories=self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex+=1
    #每次敲回车输出一个段子
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input=raw_input()
            self.loadPage()
            if input=='q':
                self.enable=False
                return
            print u"第%d页\t发布人:%s\t赞:%s  评论:%s\n%s" %(page,story[0],story[2],story[3],story[1])

    def start(self):
        print u"正在读取糗事百科,Enter键查看新段子,q退出"
        self.enable=True
        self.loadPage()
        newPage=0
        while self.enable:
            if len(self.stories)>0:
                pageStories=self.stories[0]
                newPage+=1
                #将全局list中第一个元素删除,因为已经取出
                del self.stories[0]
                self.getOneStory(pageStories,newPage)
spider=QSBK()
spider.start()
