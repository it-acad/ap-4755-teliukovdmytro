from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from authentication.models import CustomUser

def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('user_login_email')
        password = request.POST.get('password')
        
        if email:
            email = email.strip()
            
        user = CustomUser.get_by_email(email)
        
        if user and user.check_password(password):
            if user.is_active:
                login(request, user)
                return redirect('profile')
            else:
                error = "Користувач знайдений, але акаунт НЕ АКТИВНИЙ (is_active=False)!"
        else:
            error = "Невірний email або пароль"
            
    # ЦЕЙ РЯДОК МАЄ БУТИ ТУТ (вирівняний по першому if) і назва має бути login.html
    return render(request, 'authentication/login.html', {'error': error})

def register_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = int(request.POST.get('role', 0))
        
        # Викликаємо ваш статичний метод з моделі
        user = CustomUser.create(
            email=email, 
            password=password, 
            first_name=first_name, 
            last_name=last_name
        )
        
        if user:
            # Налаштовуємо роль та права користувача
            user.role = role
            if role == 1:  # Бібліотекар
                user.is_staff = True
            
            # У вашій моделі за дефолтом default=False, тому робимо його активним
            user.is_active = True  
            
            # УВАГА: save() викликається ТУТ, поза умовою (щоб зберегти ВСІХ користувачів)
            user.save() 
            
            return redirect('/auth/login/Я')
        else:
            error = "Некоректні дані або такий користувач вже існує"
            
    return render(request, 'authentication/register.html', {'error': error})
def profile_view(request):
    # Перевіряємо, чи користувач взагалі авторизований
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'authentication/profile.html')
