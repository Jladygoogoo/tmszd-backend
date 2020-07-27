from rest_framework import serializers

from results.models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = (
            'blogURL',
            'writer',
            'writerURL',
            'title',
            'abstract',
            'tags',
            'likedCount',
            'commentCount',
        )
