# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
import urllib
from jindong.items import JindongItem
class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://jd.com/']

    def parse(self, response):
    	key="手机"
    	j=3
    	for i in range(1,200,2):
    		url="https://search.jd.com/Search?keyword="+str(key)+"&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq="+str(key)+"&cid2=653&cid3=655&page="+str(i)+"&s="+str(j)+"&click=0"
    		j=j+55
    		yield Request(url=url,callback=self.page)
    		
    def page(self,response):	
    	gid=response.xpath("//li[@class='gl-item']/@data-sku").extract()
    	for i in range(0,len(gid)):
    		thisurl="https://item.jd.com/"+gid[i]+".html"
    		yield Request(url=thisurl,callback=self.next)

    def next(self,response):
    	item=JindongItem()
    	name=response.xpath("//div[@class='sku-name']/text()").extract()[0].strip()
    	goodsurl=response.url
    	goodmatch="com\/(\d*)\.html";
    	goodid=re.compile(goodmatch).findall(goodsurl)[0]
    	priceurl="https://p.3.cn/prices/mgets?callback=jQuery577058&type=1&area=1_72_2799_0&pdtk=&pduid=151395167384512824605&pdpin=&pin=null&pdbp=0&skuIds=J_"+goodid+"&ext=11000000&source=item-pc"
    	pricedata=urllib.request.urlopen(priceurl).read().decode('utf-8','ignore')
    	pircematch='"op":"(\w*\.\w*)"'
    	price=re.compile(pircematch).findall(pricedata)[0]
    	haopurl="https://club.jd.com/comment/productCommentSummaries.action?referenceIds="+goodid+"&callback=jQuery9001111&_=1513960278518"
    	haopdata=urllib.request.urlopen(haopurl).read().decode('utf-8','ignore')
    	haopmatch='"CommentCount":(\d*)'
    	haop=re.compile(haopmatch).findall(haopdata)[0]
    	item['name']=name
    	item['goodsurl']=goodsurl
    	item['price']=price
    	item['haop']=haop
    	yield item
    	
