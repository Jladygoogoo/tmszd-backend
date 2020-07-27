from djongo import models


class Comment(models.Model):
    class Meta:
        app_label = 'comments'
        abstract = True

    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=128)
    content = models.TextField()
    releaseTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DerivedComment(Comment):
    rootCommentID = models.CharField(max_length=32)


class RootComment(Comment):
    commentTags = models.CharField(max_length=256)
    derivedComments = models.ArrayField(
        model_container=DerivedComment, null=True)
