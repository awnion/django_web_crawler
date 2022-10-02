from django.shortcuts import HttpResponseRedirect, render
from .models import Crawl, Page
from .forms import CrawlerForm


def home(request):
    if request.method == 'POST':
        form = CrawlerForm(request.POST)
        if form.is_valid():
            new_crawl = Crawl(initial_url=form.cleaned_data['url'])
            new_crawl.save()
            return HttpResponseRedirect('/')

    else:
        form = CrawlerForm()

    context = {}
    context['form'] = form
    context['crawls'] = Crawl.objects.all()
    context['pages'] = Page.objects.all()
    return render(request, 'web_crawler/index.html', context)
