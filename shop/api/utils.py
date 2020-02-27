from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginations_items(items, page,item_count):
    paginator = Paginator(items, item_count)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
        page = 1
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return items, page, paginator.num_pages
