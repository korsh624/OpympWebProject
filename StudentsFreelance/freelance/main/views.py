from django.shortcuts import render

from .models import Order, Comment


def index_page(request):
    comments = Comment.objects.order_by('?')[:3]

    if comments:
        return render(request, 'index.html', context={'comments': comments})
    else:
        return render(request, 'index.html', context={'message': 'Комментариев не найдено!'})


def search_page(request):
    text = request.GET['text']
    try:
        orders = Order.objects.filter(title__icontains=text)
    except Order.DoesNotExist:
        return render(request, 'search.html', context={'message': 'Искомых заказов не найдено!'})

    return render(request, 'search.html', context={'orders': orders})


def detail_page(request, order_id):
    # order_id = request.GET['order_id']

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, 'search.html', context={'message': 'Искомых заказов не найдено!'})
    
    return render(request, 'detail.html', context={'order': order})