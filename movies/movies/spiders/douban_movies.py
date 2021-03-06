# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from movies.items import MoviesItem


class movieSpider(CrawlSpider):

   name = 'movies'
   #start_urls = ['https://movie.douban.com/subject/1292052/']
   #start_urls = ['https://movie.douban.com/subject/26836845/']
   start_urls = ['https://movie.douban.com/tag/2011']
   rules = [
      Rule(SgmlLinkExtractor(allow=(r'https://movie.douban.com/tag/2011\?start=\d+.*'))),
      Rule(SgmlLinkExtractor(allow=(r'https://movie.douban.com/subject/\d+')),callback="parse_item")
           ]
   

   def parse_item(self,response):
      
      item = MoviesItem() 
      selector = Selector(response)
      movie_detail = "".join(response.xpath("//div[@id='info']").extract() )
      id = response.url.split('/')[-2]
      title = selector.xpath('//div[@id="content"]/h1/span[1]/text()').extract()[0]
      director = "/".join(response.xpath('//a[@rel="v:directedBy"]/text()').extract())
      year = selector.xpath('//div[@id="content"]/h1/span[2]/text()').re(r'\d+')[0]
      actors = "/".join(response.xpath('//span[@class="actor"]/span[@class="attrs"]/a/text()').extract())
      genres = "/".join(response.xpath('//span[@property="v:genre"]/text()').extract())
      try:
         votes = selector.xpath('//span[@property="v:votes"]/text()').extract()[0] 
      except:
         votes = 0
      country = re.compile(ur"制片国家/地区:</span> (.+?)<br>").search(movie_detail).group(1)
      try:
         language = re.compile(ur"语言:</span> (.+?)<br>").search(movie_detail).group(1)
      except:
         language = None
      short = "".join( selector.xpath('//span[@property="v:summary"]/text()').extract() )
      try:
         rate = selector.xpath('//strong[@class="ll rating_num"]/text()').extract()[0]
      except:
         rate = 0
      try:  
         runtime = selector.xpath('//span[@property="v:runtime"]/text()').extract()[0]
      except:  
        try:
           runtime = re.compile(ur"片长:</span> (.+?)<br>").search(movie_detail).group(1)
        except:
           runtime = None
      short = re.sub('\n| +','',short)
      item['id'] = id
      item['title'] = title
      item['director'] = director
      item['year'] = year
      item['language'] = language
      item['country'] = country
      item['actor'] = actors
      item['genres'] = genres
      item['runtime'] = runtime
      item['short'] = short
      item['rate'] = rate
      item['votes'] = votes
      #return item
      yield item
      #print id,title,director,year,actors,genres,runtime,rate,votes,short,country,language
