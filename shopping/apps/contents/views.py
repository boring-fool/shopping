from django.shortcuts import render
from django.views import View


from .utils import get_categories
from .models import ContentCategory
# Create your views here.

class IndexView(View):

    def get(self, request):
        categories = get_categories()
        contents = {}
        content_categories = ContentCategory.objects.all()
        for content_category in content_categories:
            # 使用广告类别查询出该类别对应的所有的广告内容
            contents[content_category.key] = content_category.content_set.filter(status=True).order_by('sequence')
        context = {
            'categories' : categories,
            'contents' : contents
        }
        return render(request,'index.html',context=context)
