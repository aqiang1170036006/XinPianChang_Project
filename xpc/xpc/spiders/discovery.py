# -*- coding: utf-8 -*-
import re
import random
import json
import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from xpc.items import PostItem, CommentItem, ComposerItem, CopyrightItem


def strip(s):
    if s:
        return s.strip()


cookies = {
    'Authorization': '666DD5194451C1B454451C4C9D4451CA0244451C0CD267080B35',
}


def gen_sessid():
    letters = [chr(i) for i in range(97, 97 + 26)] + [str(i) for i in range(10)]
    return random.choices(letters, k=26)


class DiscoverySpider(RedisSpider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com', 'openapi-vtom.vmovier.com']
    start_urls = ['https://www.xinpianchang.com/channel/index/type-/sort-like/duration_type-0/resolution_type-/page-1']

    def parse(self, response):
        url = 'https://www.xinpianchang.com/a%s?from=ArticleList'
        # pid_list = response.xpath('//ul[@class="video-list"]/li/@data-articleid').extract()
        post_list = response.xpath('//ul[@class="video-list"]/li')
        for post in post_list:
            pid = post.xpath('./@data-articleid').get()
            req = Request(url % pid, callback=self.parse_post)
            req.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            req.meta['pid'] = pid
            yield req
        next_page = response.xpath('//div[@class="page"]/a[last()]/@href').get()
        if next_page:
            cookies['PHPSESSID'] = gen_sessid()
            yield response.follow(next_page, callback=self.parse, cookies=cookies)

    def parse_post(self, response):
        post = PostItem()
        pid = response.meta['pid']
        post['pid'] = pid
        # 视频标题
        post['title'] = response.xpath('//h3[contains(@class, "title")]/text()').extract_first()
        # 缩略图
        post['thumbnail'] = response.meta['thumbnail']

        # 分类
        cates = response.xpath('//span[contains(@class, "cate")]//text()').extract()
        post['category'] = ''.join([strip(cate) for cate in cates])
        # 创建时间
        post['created_at'] = response.xpath('//span[contains(@class, "update-time")]/i/text()').get()
        # 播放次数
        post['play_counts'] = response.xpath('//i[contains(@class, "play-counts")]/@data-curplaycounts').get()
        # 点赞次数
        post['like_counts'] = response.xpath('//span[contains(@class, "like-counts")]/@data-counts').get()
        # 介绍
        post['description'] = strip(response.xpath('//p[contains(@class, "desc")]/text()').get())

        video_url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource&usage=xpc_web'
        vid, = re.findall(r'vid: \"(\w+)\"', response.text)
        post['vid'] = vid
        req = Request(video_url % vid, callback=self.parse_video)
        req.meta['post'] = post
        yield req

        comment_url = 'https://app.xinpianchang.com/comments?resource_id=%s&type=article&page=1' % pid

        req = Request(comment_url, callback=self.parse_comments)
        yield req

        # 爬取用户页面
        # composer_urls = response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li/a/@href').extract()
        composers = response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li')

        for composer in composers:
            cid = composer.xpath('./a/@data-userid').get()
            req = response.follow(composer.xpath('./a/@href').get(), callback=self.parse_composer)
            # 不跟踪此页面的cookie，以防止visit_userid_10043764这样的cookie泛滥
            req.meta['dont_merge_cookies'] = True
            yield req
            # 获取作品与作者的对应关系
            cr = CopyrightItem()
            cr['pcid'] = '%s-%s' % (pid, cid)
            cr['pid'] = pid
            cr['cid'] = cid
            cr['roles'] = composer.xpath('.//span[contains(@class, "roles")]/text()').get()
            yield cr

    def parse_video(self, response):
        """处理视频接口"""
        resp = json.loads(response.text)
        post = response.meta['post']
        post['video'] = resp['data']['resource']['default']['url']
        # 背景图
        post['banner'] = resp['data']['video']['cover']
        post['duration'] = resp['data']['video']['duration']
        yield post

    def parse_comments(self, response):
        """处理评论接口"""
        resp = json.loads(response.text)
        for c in resp['data']['list']:
            comment = CommentItem()
            comment['id'] = c['id']
            comment['content'] = c['content']
            comment['created_at'] = c['addtime']
            comment['pid'] = c['resource_id']
            comment['cid'] = c['userid']
            comment['avatar'] = c['userInfo']['avatar']
            comment['uname'] = c['userInfo']['username']
            comment['like_counts'] = c['count_approve']
            comment['referid'] = c['referid']
            yield comment

        next_page_url = resp['data']['next_page_url']
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_comments)

    def parse_composer(self, response):
        composer = ComposerItem()
        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()
        composer['cid'] = response.xpath('//div[@class="creator-info"]//span/@data-userid').get()
        composer['banner'], = re.findall(r'background-image:url\((.+?)\)', banner)
        composer['avatar'] = response.xpath('//span[@class="avator-wrap-s"]/img/@src').get()
        composer['verified'] = response.xpath('//span[@class="avator-wrap-s"]/span/@class').get()
        composer['name'] = response.xpath('//p[contains(@class, "creator-name")]/text()').get()
        composer['intro'] = response.xpath('//p[contains(@class, "creator-desc")]/text()').get()
        like_counts = response.xpath('//span[contains(@class, "like-counts")]/text()').get()
        like_counts = like_counts.replace(',', '') if like_counts else ''
        composer['like_counts'] = like_counts
        composer['fans_counts'] = response.xpath('//span[contains(@class, "fans-counts")]/@data-counts').get()
        composer['follow_counts'] = response.xpath('//span[@class="follow-wrap"]/span[2]/text()').get()
        composer['location'] = response.xpath(
            '//span[contains(@class,"icon-location")]/following-sibling::span[1]/text()').get()
        composer['career'] = response.xpath(
            '//span[contains(@class,"icon-career")]/following-sibling::span[1]/text()').get()
        # from scrapy.shell import inspect_response
        # if composer['banner'] is None:
        #     inspect_response(response, self)
        yield composer