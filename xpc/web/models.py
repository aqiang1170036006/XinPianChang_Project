# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.BigIntegerField()
    cid = models.BigIntegerField()
    avatar = models.CharField(max_length=512, blank=True, null=True)
    uname = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
    like_counts = models.IntegerField()
    referid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comments'


class Composer(models.Model):
    cid = models.BigIntegerField(primary_key=True)
    banner = models.CharField(max_length=512)
    avatar = models.CharField(max_length=512)
    verified = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=128)
    intro = models.TextField(blank=True, null=True)
    like_counts = models.IntegerField()
    fans_counts = models.IntegerField()
    follow_counts = models.IntegerField()
    location = models.CharField(max_length=32, blank=True, null=True)
    career = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'composers'

    @property
    def posts(self):
        cr_list = Copyright.objects.filter(cid=self.cid).all()
        posts = []
        for cr in cr_list:
            post = Post.objects.get(pid=cr.pid)
            post.roles = cr.roles
            posts.append(post)
        return posts


class Copyright(models.Model):
    pcid = models.CharField(primary_key=True, max_length=32)
    pid = models.BigIntegerField()
    cid = models.BigIntegerField()
    roles = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'copyrights'


class Post(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    banner = models.CharField(max_length=512, blank=True, null=True)
    video = models.CharField(max_length=512, blank=True, null=True)
    category = models.CharField(max_length=512)
    created_at = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    play_counts = models.IntegerField()
    like_counts = models.IntegerField()
    thumbnail = models.CharField(max_length=512, blank=True, null=True)
    duration = models.IntegerField()
    vid = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'

    @property
    def durations(self):
        return "%s' %s''" % divmod(self.duration // 1000, 60)

    @property
    def readable_play_counts(self):
        a, b = divmod(self.play_counts, 10000)
        if not a:
            return self.play_counts
        return '%s.%sw' % (a, b // 1000) if b // 1000 else '%sw' % a

    @property
    def readable_like_counts(self):
        a, b = divmod(self.like_counts, 10000)
        if not a:
            return self.like_counts
        return '%s.%sw' % (a, b // 1000) if b // 1000 else '%sw' % a

    @property
    def composers(self):
        cr_list = Copyright.objects.filter(pid=self.pid).all()
        composers = []
        for cr in cr_list:
            composer = Composer.objects.get(cid=cr.cid)
            composer.roles = cr.roles
            composers.append(composer)
        return composers