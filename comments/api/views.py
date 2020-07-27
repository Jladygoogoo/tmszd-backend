from rest_framework.generics import ListAPIView
from comments.models import RootComment
from .serializers import CommentSerializer


class CommentListView(ListAPIView):
    queryset = RootComment.objects.all()
    serializer_class = CommentSerializer
