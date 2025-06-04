from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Phone


def get_phones(MyPhone):
    return [{
        'id': c.id,
        'name': c.name,
        'price': c.price,
        'release_date': c.release_date,
        'lte_exists': c.lte_exists,
        'slug': c.slug,
        'image': c.image,
    } for c in MyPhone.objects.all()]


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_by = request.GET.get('sort', None)
    phones = get_phones(Phone)
    match sort_by:
        case 'name':
            phones.sort(key=lambda d: d['name'])
        case 'min_price':
            phones.sort(reverse=False, key=lambda d: d['price'])
        case 'max_price':
            phones.sort(reverse=True, key=lambda d: d['price'])

    context = {'phones': phones, 'sort_by': sort_by}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phones = get_phones(Phone)
    phone = [my_phone for my_phone in phones if my_phone['slug'] == slug]
    context = {'phone': phone[0]}
    return render(request, template, context)


def list_phones(request):
    phone_objects = Phone.objects.all()
    phones = [f'{c.id}: {c.name}, {c.price} date: {c.release_date} | {c.lte_exists} {c.slug}' for c in phone_objects]
    return HttpResponse('<br>'.join(phones))