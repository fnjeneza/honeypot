from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html',{'last_urls':['tet','de']})

def received(request):
    return render(request,'received.html')
