from rest_framework import serializers

from comments.models import RootComment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RootComment
        fields = ('title', 'content', 'releaseTime',
                  'commentTags')
