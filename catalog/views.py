from django.shortcuts import render


def home(request):
    return render(request, template_name='home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('answer.txt', 'a+', encoding='utf-8') as file:
            file.write(f'\n{name}({phone}): {message}\n')
    return render(request, template_name='contacts.html')
