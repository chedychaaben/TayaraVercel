from django.shortcuts import render, HttpResponse

# Create your views here.
def login(request):
    context = {

    }
    return render(request,'login.html', context=context)