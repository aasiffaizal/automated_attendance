from django.http import HttpResponse, Http404, HttpResponseRedirect

def index(request):
    return HttpResponseRedirect("/login/")

    
