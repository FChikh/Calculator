import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView

# Create your views here.
from firstapp.forms import CalcForm
from firstapp.models import CalcHistory


@login_required
def calc(request):
    # Базовый контекст
    print(request.user)
    context = dict()
    history = CalcHistory.objects.all()
    context['history'] = history
    if request.method == 'POST':
        f = CalcForm(request.POST)
        if f.is_valid():
            # обработка вычисления
            a = f.data['first']
            b = f.data['second']
            c = int(a) + int(b)

            # формирование ответа
            context['first'] = a
            context['second'] = b
            context['result'] = c
            context['form'] = f
            # добавление элемента в БД
            item = CalcHistory(date=datetime.datetime.now(),
                               first=a,
                               second=b,
                               result=c,
                               author=request.user)
            item.save()

        else:
            context['form'] = CalcForm()
    else:
        # получение GET-параметра delete, если мы хотим что-то удалить
        req = request.GET.get('delete', '')
        if req != '':
            # поиск ответа по заданному фильтру
            item = CalcHistory.objects.filter(id=int(req))
            print(item)

            # получить массив объектов, удовлетворяющих условию фильтра
            # item = CalcHistory.objects.filter(id=int(req)).values()
            item.delete()
        context['nothing_entered'] = True
        context['form'] = CalcForm()
        context['first'] = 0
        context['second'] = 0
        context['result'] = 0
    return render(request, 'calculator.html', context)


def index(request):
    return redirect("/calc")


def logout_view(request):
    logout(request)
    return redirect("/login/")


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
