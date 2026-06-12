from django.http import HttpResponse

def author_list(request):
    # Тест шукає саме цей рядок у відповіді сторінки!
    return HttpResponse("This is author app page! Congratulations!")
# Create your views here.
