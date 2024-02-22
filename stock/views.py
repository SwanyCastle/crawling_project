from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Max
from django.contrib import messages

from django.http import JsonResponse 

from .crawl import crawling_data
from .models import Data, FirmData


def list_data(request):
    page = request.GET.get('page', '1')
    firm_select = request.GET.get('trading_firm_select', None)
    s_date = request.GET.get('s_date', None)
    e_date = request.GET.get('e_date', None)

    if not firm_select:
        crawled_datas = Data.objects.order_by('-close_date')       
    elif firm_select == 'KB증권': 
        crawled_datas = Data.objects.filter(Q(trading_firm__icontains=firm_select)|Q(trading_firm__icontains='케이비')).order_by('-close_date')
    elif firm_select == 'IBK투자증권':
        crawled_datas = Data.objects.filter(Q(trading_firm__icontains=firm_select)|Q(trading_firm__icontains='아이비케이투자')).order_by('-close_date')
    else:
        crawled_datas = Data.objects.filter(trading_firm__icontains=firm_select).order_by('-close_date')

    if s_date is None or e_date is None:
        s_date = ""
        e_date = ""

    if s_date or e_date:
        if not s_date:
            crawled_datas = crawled_datas.filter(close_date__lte=e_date).order_by('-close_date')
        elif not e_date:
            crawled_datas = crawled_datas.filter(open_date__gte=s_date).order_by('-close_date')
        else:
            crawled_datas = crawled_datas.filter(open_date__gte=s_date, close_date__lte=e_date).order_by('-close_date')

    if not crawled_datas:
        crawled_datas = Data.objects.order_by('-close_date')
        messages.warning(request, f'데이터가 존재하지 않습니다.')
    firm_data = FirmData.objects.order_by('id')
    paginator = Paginator(crawled_datas, 15)
    page_obj = paginator.get_page(page)
    context = {
        'crawled_datas': page_obj, 
        'firm_data': firm_data, 
        'date_time': timezone.now(), 
        'end_page': paginator.num_pages,
        'firm_select': firm_select,
        'start_date': s_date,
        'end_date': e_date
    }
    return render(request, "stock/crawldata_list.html", context)

# csrf 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def load_data(request):
    crawling_data()
    update_datetime = Data.objects.aggregate(crawled_datetime=Max('crawled_datetime'))
    context = {'last_update': update_datetime}
    return JsonResponse(context)

@csrf_exempt
def delete_data(request):
    chk_rows = request.POST.getlist('chk_rows[]')
    for i in chk_rows:
        if i.isdigit():
            row = Data.objects.get(id=i)
            row.delete()
    return redirect('stock:list_data')