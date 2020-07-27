from django.db import models


class Tag(models.Model):
    tagName = models.CharField(max_length=32, primary_key=True)
    lastUpdate = models.DateTimeField()

    def __str__(self):
        return self.tagName


class Result(models.Model):
    # 文章网址
    blogURL = models.URLField()
    # 文章id（从网址中提取）
    blogID = models.CharField(max_length=64, primary_key=True, default='-')
    # 作者昵称
    writer = models.CharField(max_length=128)
    # 作者主页网址
    writerURL = models.URLField()
    # 文章标题
    title = models.CharField(max_length=128)
    # 文章简介
    abstract = models.TextField()
    # 点赞数
    likedCount = models.IntegerField()
    # 评论数
    commentCount = models.IntegerField()
    # 文章包含的tags
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
