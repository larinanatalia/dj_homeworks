from collections import Counter
from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся


counter_click = Counter()
counter_show = Counter()

def index(request):
    link_from = request.GET.get('from-landing','')
    if link_from == '':
        return render(request, 'index.html')
    if link_from == 'original':
        counter_click[link_from] += 1
        return render(request, 'index.html')
    if link_from == 'test':
        counter_click[link_from] += 1
        return render(request, 'index.html')
    return counter_click


def landing(request):
    version = request.GET['ab-test-arg']
    if version == 'original':
        counter_show[version] += 1
        return render(request, 'landing.html')
    if version == 'test':
        counter_show[version] += 1
        return render(request, 'landing_alternate.html')
    return counter_show


def stats(request):
    test_conversion = round(counter_click['test']/counter_show['test'], 1)
    original_conversion = round(counter_click['original'] / counter_show['original'], 1)
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
