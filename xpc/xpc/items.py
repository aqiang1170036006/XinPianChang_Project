# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class PostItem(scrapy.Item):
    table_name = 'posts'
    pid = Field()
    title = Field()
    thumbnail = Field()
    category = Field()
    created_at= Field()
    play_counts= Field()
    like_counts= Field()
    description= Field()
    video = Field()
    banner = Field()
    vid = Field()
    duration = Field()


class CommentItem(scrapy.Item):
    table_name = 'comments'
    id = Field()
    content= Field()
    created_at = Field()
    pid = Field()
    cid = Field()
    like_counts = Field()
    referid = Field()
    avatar = Field()
    uname = Field()


class ComposerItem(scrapy.Item):
    table_name = 'composers'
    cid = Field()
    banner = Field()
    avatar = Field()
    verified = Field()
    name = Field()
    intro = Field()
    like_counts = Field()
    fans_counts = Field()
    follow_counts = Field()
    location = Field()
    career = Field()


class CopyrightItem(scrapy.Item):
    table_name = 'copyrights'
    pcid = Field()
    pid = Field()
    cid = Field()
    roles = Field()