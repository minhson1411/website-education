from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout

#ham dang ky
def REGISTER(request):
    if request.method == "POST":
        #tao 3 bien
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check email
        if User.objects.filter(email = email).exists():
            messages.warning(request, 'Email đã được dùng!')
            return redirect('register')

        #check tai khoan
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Tài khoản đã được dùng!')
            return redirect('register')

        user = User(
            username = username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request,'registration/register.html')

#ham dang nhap
def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user =  EmailBackEnd.authenticate(request, username=email, password=password)
        if user != None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Email và mật khẩu không hợp lệ!')
            return redirect('login')

def PROFILE(request):
    return render(request,'registration/profile.html')

def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_id = request.user.id

        user = User.objects.get(id=user_id)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)

        user.save()
        messages.success(request, 'Cập nhật thành công.')
        return redirect('profile')