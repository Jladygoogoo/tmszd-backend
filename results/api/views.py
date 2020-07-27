from rest_framework.generics import ListAPIView, RetrieveAPIView

from results.models import Tag
from .serializers import ResultSerializer

from .utils import updateTagData


class ResultListView(ListAPIView):
    serializer_class = ResultSerializer

    def get_queryset(self):
        # 使用Tag实例对象作为匹配参数，查找所有对应文章
        tagName = self.request.path.split('/')[-1]
        if 'update' in self.request.GET:
            update = self.request.GET['update']
        else:
            update = 0

        print("ResultListView.get_queryset - tagName:", tagName)

        tag = Tag.objects.filter(tagName=tagName)
        if tag and (not update):
            return tag[0].result_set.all()
        else:
            updateTagData(tagName)
            tag = Tag.objects.get(tagName=tagName)
            return tag.result_set.all()
