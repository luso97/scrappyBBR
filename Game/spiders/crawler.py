'''
Created on 2 ene. 2019

@author: Luis
'''
import scrapy
import re;
from scrapy.selector import Selector ;

class spider(scrapy.Spider):
    name = "games"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ['https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2005&year_max=2017&is_range=N&game_num_type=team&order_by=date_game']

    def parse(self, response):
        #self.log('I just visited: ' + response.url)
        limit=5;
        j=1;   
        for game in response.css('tbody tr'):
            url =game.css('td[data-stat=team_id] > a::attr(href)').extract_first();
            url = response.urljoin(url);
            item={};
            item['HOM']= game.css('td[data-stat=team_id] ::text').extract_first();
            wl=game.css('td[data-stat=game_result] ::text').extract_first();
            item['H']=0;
            item['L']=1;
            date=game.css('td[data-stat=date_game] ::text').extract_first();
            if re.search("W", wl):
                item['H']=1;
                item['L']=0;
            url2 =game.css('td[data-stat=opp_id] > a::attr(href)').extract_first();
            #print("URL2",url2);    
            x=scrapy.Request(url=url, callback=self.parseTeamStats,meta={'date':date,'url2':url2});
            x.meta['item'] = item
            #Away team
        
            yield x;
        #=======================================================================
        # response.xpath('//strong[contains(.,"PTS/G:")]/following-sibling::text()[1]')
        #=======================================================================
        next_page_url = response.xpath('//a[contains(.,"Next")]/@href').extract_first();
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
    def start_requests(self):
        urls =['https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2005&year_max=2017&is_range=N&game_num_type=team&order_by=date_game'];
        for url in urls:
            print(url);
            yield scrapy.Request(url=url, callback=self.parse)    
    def parseTeamStats(self,response):
        item = response.meta['item']
        url2=response.meta['url2'];
        date=response.meta['date'];
        print("DATE",date)
        url =response.xpath('//a[contains(.,"Schedule & Results")]/@href').extract_first();
        url = response.urljoin(url);
        url2=response.urljoin(url2);
        #homeTeamPTSPERGAME
        d=response.xpath('//strong[contains(.,"PTS/G:")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['PTSGH']=m[0];
        d=response.xpath('//strong[contains(.,"Opp PTS/G:")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['OPPPTSGH']=m[0];
        d=response.xpath('//strong[contains(.,"Pace")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['PACEH']=m[0];
        d=response.xpath('//strong[contains(.,"Off Rtg")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['OFFH']=m[0];
        d=response.xpath('//strong[contains(.,"Def Rtg")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['DEFH']=m[0];
        x=scrapy.Request(url=url, callback=self.parseTeamGames,meta={'date':date,'url2':url2});
        x.meta['item'] = item
        #return item;
        return x;
    def parseOppTeamStats(self,response):
        print("ehem");
        item = response.meta['item']
        date=response.meta['date'];
        print("DATE",date)
        url =response.xpath('//a[contains(.,"Schedule & Results")]/@href').extract_first();
        url = response.urljoin(url);
        #homeTeamPTSPERGAME
        d=response.xpath('//strong[contains(.,"PTS/G:")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['PTSGA']=m[0];
        d=response.xpath('//strong[contains(.,"Opp PTS/G:")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['OPPPTSGA']=m[0];
        d=response.xpath('//strong[contains(.,"Pace")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['PACEA']=m[0];
        d=response.xpath('//strong[contains(.,"Off Rtg")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['OFFA']=m[0];
        d=response.xpath('//strong[contains(.,"Def Rtg")]/following-sibling::text()[1]').extract_first();
        m=re.findall("\d+\.\d",d);
        item['DEFA']=m[0];
        x=scrapy.Request(url=url, callback=self.parseOppTeamGames,meta={'date':date});
        x.meta['item'] = item
        #return item;
        return x;
    def parseTeamGames(self,response):
        date=response.meta['date'];
        url2=response.meta['url2'];
        print("ezz",url2)
        print("DATE2",date)
        item = response.meta['item'];
        xpath1='//tr[td[contains(@csk,"%s")]]' % date;
        print("xapth1",xpath1)
        string=response.xpath(xpath1).extract_first();
        print("STR",string);
        hxs = Selector(text=string) ;
        m=hxs.xpath('//th[contains(@data-stat,"g")]/text()').extract_first();
        print("MMM",m)
        res=0;
        if m==1:
            res=0;
        else:
            mint=int(m);
            mint=mint-1;
            mint=str(mint);
            xpath1='//tr[th[contains(.,"%s")]]' % mint;
            print(xpath1);
            d=response.xpath(xpath1).extract_first();
            hxs2=Selector(text=d);
            u=hxs2.css('td[data-stat="game_streak"]::text').extract_first();
            print("U",u);
            res=re.findall("\d+",u );
            res2=re.findall("W|L",u);
            if res2[0]=="W":
                res=res[0];
            if res2[0]=="L":
                r='-%s'%res[0];
                res=r;
            print (res);
            
        
        item['STREAKH']=res;  
        print("url2222",url2)  
        x=scrapy.Request(url=url2, callback=self.parseOppTeamStats,meta={'date':date});
        print("aqui salen cosas");
        x.meta['item'] = item
        #return item;
        return x;   
    def parseOppTeamGames(self,response):
        date=response.meta['date'];
        print("DATE2",date)
        item = response.meta['item'];
        xpath1='//tr[td[contains(@csk,"%s")]]' % date;
        print("xapth1",xpath1)
        string=response.xpath(xpath1).extract_first();
        print("STR",string);
        hxs = Selector(text=string) ;
        m=hxs.xpath('//th[contains(@data-stat,"g")]/text()').extract_first();
        print("MMM",m)
        res=0;
        if m==1:
            res=0;
        else:
            mint=int(m);
            mint=mint-1;
            mint=str(mint);
            xpath1='//tr[th[contains(.,"%s")]]' % mint;
            print(xpath1);
            d=response.xpath(xpath1).extract_first();
            hxs2=Selector(text=d);
            u=hxs2.css('td[data-stat="game_streak"]::text').extract_first();
            print("U",u);
            res=re.findall("\d+",u );
            res2=re.findall("W|L",u);
            if res2[0]=="W":
                res=res[0];
            if res2[0]=="L":
                r='-%s'%res[0];
                res=r;
            print (res);
        item['STREAKA']=res;    
        
        
        return item;   