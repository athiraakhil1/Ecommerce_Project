from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,FileResponse
from django.views.decorators.cache import cache_control
from website.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.
def login_view(request):
    if request.method=="POST":
      em=request.POST.get('email')
      ps=request.POST.get('password')
      user=authenticate(email=em,password=ps)
      if user is not None:
       if user.is_superuser:
         login(request,user)
         return redirect('dashview')
       else:
         return redirect('login')
    return render(request,"index/login.html")


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
   notify=Notification.objects.all().order_by('-id')[:4]
   notify_count=Notification.objects.filter(is_read=False).count() 
   return render(request,"index/dashboard.html",{'notify':notify,'notify_count':notify_count})
   
def mark_as_read(request,notification_id) :
   notification=get_object_or_404(Notification,id=notification_id) 
   notification.is_read=True
   notification.save() 
   return redirect('dashview')