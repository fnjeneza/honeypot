from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

from honeypot_web.models import Broker



# Create your views here.
def index(request):
    url_spammer = request.POST.get('url_spammer', None)
    
    if url_spammer :
        broker = Broker(url=url_spammer,
                processed = False
                )
        broker.save()
    
    broker = Broker.objects.all()
    urls = [br.url for br in broker]
    messages.add_message(request,messages.INFO, "url a été ajouté")
    return render(request, 'index.html',{'last_urls':urls})

def received(request):
    url = request.POST['url_spammer']
    print('url spammer %s' % url)
    return render(request,'received.html')
