import os

from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Sum, Q
from django.db.models.query import RawQuerySet
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Advertisement, Stat, Comment
from .forms import AdvertisementForm, Tst
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import View
from .signals import *


def logout_view(request):
    logout(request)
    return redirect('home')


from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate


def signup(request):
    ''' Добавление пользовтеля в БД'''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    ''' генерация начальной страницы'''
    return render(request, 'home.html')


def advertisement_list(request):
    ''' вывод из БД списа объявлений'''
    # advertisements = Advertisement.objects.all()
    all = Advertisement.votes.count()
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements}, )


def advertisement_detail(request, pk):
    ''' вывод деталей объявления, номер которого хранится в pk'''
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})


@login_required
def add_advertisement(request):
    ''' добавление объявления'''

    global user_id
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            if not advertisement.image:
                # Обрабатываем отсутствие файла, ставим заглушку
                advertisement.image = 'advertisements/none.jpg'

            advertisement.save()
            # update_advertisement_count(sender=Advertisement, instance=advertisement, created=True)

            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    ''' редактирование переданного обьявления  '''
    advertisement = Advertisement.objects.get(pk=pk)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            form.instance.author = request.user
            img_obj = form.instance
            form.save()
            return redirect('board:advertisement_detail', pk=img_obj.pk)
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'board/edit_advertisement.html', {'form': form, 'advertisement': advertisement})


def vote_advertisement(request, post_id):
    ''' функция голосования пользователя и записывает в БД результат'''
    if request.method == 'POST':
        post = get_object_or_404(Advertisement, id=post_id)
        # Проверка, залогинен ли пользователь
        # Голосование
        action = request.POST.get('action')  # 'up' or 'down'
        post.vote(request.user, action)
        post.save()
        return redirect('board/advertisement_list_old.html', pk=post.id)

    return HttpResponseBadRequest()


@login_required
def del_advertisement(request, pk):
    ''' удаление записи, при удалении записис сохраняет файл заглушку'''
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.user != advertisement.author:
        return redirect('board:advertisement_list')  # если пользователь не является автором
    if request.method == "POST":

        file_path = advertisement.get_image_full_path()
        file_name = str(advertisement.get_image_name())
        if 'none.jpg' not in file_name:
            advertisement.delete()
            os.remove(file_path)
        else:
            advertisement.delete()

        return redirect('board:advertisement_list')

    return redirect('board:advertisement_detail', pk=pk)

@login_required
def stat_advertisement(request):
    ''' вывод статистики по каждому пользователю в разрезе имя, сколько постов, сколько лайков дизлайков '''
    author_stats = get_author_stats()
    context = {"author_stats": author_stats}
    return render(request, 'stat_advertisement.html', context)

def get_author_stats():
    # # Получаем статистику по каждому автору
    queryset = (Advertisement.objects.values('author_id__username').
                annotate(Count('author_id'), Sum('num_vote_up'), Sum('num_vote_down'),Sum('vote_score') ))

    return list(queryset)





class VoteView(View):
    ''' класс, содержит метод, который отрабатывает голосование и возвращает результат голосования в форму'''

    def post(self, request, advertisement_id, action):
        advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
        if action == 'up':
            advertisement.votes.up(advertisement_id)
        elif action == 'down':
            advertisement.votes.down(advertisement_id)
        else:
            return redirect('board:advertisement_list')
        return redirect('board:advertisement_list')

def advertisement_list(request):
    '''
    Отображение списка объявлений с пагинацией.
    '''
    # Получаем все объявления
    advertisements = Advertisement.objects.all()

    # Пагинация
    paginator = Paginator(advertisements, 5)
    page = request.GET.get('page')

    try:
        # Получаем объявления для текущей страницы
        advertisements_page = paginator.page(page)
    except PageNotAnInteger:
        # Если page не является числом, показываем первую страницу
        advertisements_page = paginator.page(1)
    except EmptyPage:
        # Если page находится за пределами диапазона, показываем последнюю страницу
        advertisements_page = paginator.page(paginator.num_pages)

    return render(request, 'board/1_advertisement_list.html', {
        'advertisements_page': advertisements_page
    })