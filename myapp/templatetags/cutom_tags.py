from django import template
from myapp.models import Request, Trackinghistory
register = template.Library()

@register.simple_tag
def pendin(data, data2):
    pend = Request.objects.filter(status='Approved')
    return pend

@register.simple_tag
def total(qty1, qty2, qty3):
    return int(qty1) + int(qty3) + int(qty2)

@register.simple_tag
def pendingbook(data, data2):
    pending = Request.objects.filter(status='Not Updated Yet')
    return pending

@register.filter(name='findreportyear')
def findreportyear(year):
    data = Trackinghistory.objects.filter(creationdate__year=year)
    total = 0
    for i in data:
        total += int(i.othercharge) + int(i.partcharge) + int(i.servicecharge)
    return total

@register.filter(name='findreportmonth')
def findreportmonth(month):
    data = Trackinghistory.objects.filter(creationdate__month=month)
    total = 0
    for i in data:
        total += int(i.othercharge) + int(i.partcharge) + int(i.servicecharge)
    return total

@register.filter(name='findmonth')
def findmonth(month):
    li = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return li[month-1]