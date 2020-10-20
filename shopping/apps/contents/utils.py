from goods.models import GoodsChannel

def get_categories():
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    categories = {}
    for channel in channels:
        group_id = channel.group_id  # 当前组

        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        category = channel.category  # 当前频道的类别

        # 追加当前频道
        categories[group_id]['channels'].append({
            'id': category.id,
            'name': category.name,
            'url': channel.url
        })
        for category2 in category.subs.all():
            category2.sub_cats = []
            for category3 in category2.subs.all():
                category2.sub_cats.append(category3)
            categories[group_id]['sub_cats'].append(category2)
    return categories