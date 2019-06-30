'''
Created on 2 ene. 2019

@author: Luis
'''
import scrapy


class spider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ['https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2005&year_max=2017&is_range=N&game_num_type=team&order_by=date_game']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for game in response.css('.sortable stats_table now_sortable>tbody>tr[data-row]'):
            item = {
                'HOM': game.css('td[data-stat=team_id::text').extract_first(),
            }
            yield item;
    def start_requests(self):
        urls =start_urls;
        for url in urls:
            print(url);
            yield scrapy.Request(url=url, callback=self.parse)    
sp=spider();
    
d=sp.start_requests();