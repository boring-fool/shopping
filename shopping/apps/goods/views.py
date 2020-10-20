import datetime
from logging import getLogger
from django.utils import timezone
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator,EmptyPage
from django import http

from contents.utils import get_categories
from .utils import get_breadcrumb
from shopping.utils.response_code import RETCODE
from .models import GoodsCategory,SKU,GoodsVisitCount

# Create your views here.
logger = getLogger('django')
class ListView(View):
    def get(self,request,category_id,page_num):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('参数category_id不存在')
        sort = request.GET.get('sort', 'default')
        if sort == 'price':
            sort_field = 'price'
        elif sort == 'hot':
            sort_field = '-sales'
        else:
            sort = 'default'
            sort_field = 'create_time'
        categories = get_categories()
        breadcrumb = get_breadcrumb(category)
        skus = category.sku_set.filter(is_launched=True).order_by(sort_field)
        paginator = Paginator(skus, 5)  # 把skus进行分页，每页5条记录
        try:
            page_skus = paginator.page(page_num)  # 获取到page_num页中的五条记录
        except EmptyPage:
            return http.HttpResponseNotFound('Empty Page')
        # 获取总页数：前端的分页插件需要使用
        total_page = paginator.num_pages

        # 构造上下文
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'page_skus': page_skus,
            'total_page': total_page,
            'page_num': page_num,
            'sort': sort,
            'category_id': category_id
        }

        return render(request,'list.html', context)
class HotGoodsView(View):
    def get(self,request,category_id):
       skus = SKU.objects.filter(category_id=category_id,is_launched=True).order_by('-sales')[:2]
       hot_skus = {}
       hot_skus = []
       for sku in skus:
           hot_skus.append({
               'id': sku.id,
               'default_image_url': sku.default_image.url,
               'name': sku.name,
               'price': sku.price
           })

       return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'hot_skus': hot_skus})
class DetailView(View):
    """商品详情页"""

    def get(self, request, sku_id):
        """提供商品详情页"""
        # 获取当前sku的信息
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return render(request, '404.html')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(sku.category)

        # 构建当前商品的规格键
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格信息
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options

        # 渲染页面
        context = {
            'categories':categories,
            'breadcrumb':breadcrumb,
            'sku':sku,
            'specs': goods_specs,
        }
        return render(request, 'detail.html', context)
class DetailVisitView(View):
    """详情页分类商品访问量"""

    def post(self, request, category_id):
        """记录分类商品访问量"""
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('缺少必传参数')

        # 获取今天的日期
        t = timezone.localtime()
        today_str = '%d-%02d-%02d' % (t.year, t.month, t.day)
        today_date = datetime.datetime.strptime(today_str, '%Y-%m-%d')
        try:
            # 查询今天该类别的商品的访问量
            counts_data = category.goodsvisitcount_set.get(date=today_date)
        except GoodsVisitCount.DoesNotExist:
            # 如果该类别的商品在今天没有过访问记录，就新建一个访问记录
            counts_data = GoodsVisitCount()

        try:
            counts_data.category = category
            counts_data.count += 1
            counts_data.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('服务器异常')

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
