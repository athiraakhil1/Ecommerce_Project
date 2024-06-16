from django.shortcuts import render,redirect
from website.models import*
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,FileResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def home_page(request):
    return render(request,"user/homepage.html")


@login_required(login_url='loginuser')
def user_login(request):
    if request.method== 'POST':
        em=request.POST.get('uemail')
        ph=request.POST.get('uphone')
        ps=request.POST.get('upassword')
        user= authenticate(email=em, password=ps)
        print(user)
        if user is not None:
            if not user.is_superuser:
                login(request, user)
                return render(request,"user/homepage.html",{'user':user})
            else:
                return redirect('firstpage')
       
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_user(request):
    response = HttpResponseRedirect('firstpage')
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    logout(request)
    request.session.flush()
    return response


def user_register(request):
    if request.method =="POST":
        registername=request.POST.get('sname')
        registeremail=request.POST.get('semail')
        registerphone=request.POST.get('sphone')
        registerpassword=request.POST.get('spassword')
        
        if User.objects.filter(email=registeremail).exists():
            msg1 = 'Email already taken try another one'
            return render(request, "user/homepage.html", {'sname': registername, 'semail': registeremail, 'sphone': registerphone, 'msg1': msg1, })
        if User.objects.filter(phone=registerphone).exists():
            msg2 = 'Phone Number already taken try another one'
            return render(request, "user/homepage.html", {'sname': registername, 'semail': registeremail, 'sphone': registerphone, 'msg2': msg2, })
        else:
          User.objects.create_user(username=registername,email=registeremail,phone=registerphone,password=registerpassword)
          message=f"A Customer {registername} with {registeremail} has created new account."
          Notification.objects.create(message=message)
        return redirect('firstpage')