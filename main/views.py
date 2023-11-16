from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, RedirectView

from .forms import AddPostForm, ReservationForm
from .models import News, Menu, Reservation, Hall
from .utils import DataMixin


def login_view(request):
    return render(request, template_name='user/login.html')


class ChaletHome(DataMixin, ListView):
    template_name = 'main/includes/index.html'
    context_object_name = 'posts'
    model = 'News'
    queryset = News.objects.all()
    title_page = 'Главная страница'


class MenuHome(DataMixin, ListView):
    template_name = 'main/includes/index_menu.html'
    context_object_name = 'posts'
    model = 'Menu'
    queryset = Menu.objects.all()
    title_page = 'Меню'


@login_required
def about(request):
    contact_list = News.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/includes/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'main/includes/news.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(News.published, slug=self.kwargs[self.slug_url_kwarg])


def page_not_found(request):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class ShowPostMenu(DataMixin, DetailView):
    template_name = 'main/includes/menu.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Menu.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/includes/addpage.html'
    title_page = 'Добавление статьи'
    permission_required = 'news.add_news'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = News
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'main/includes/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'main.change_main'


@permission_required(perm='main.add_news', raise_exception=True)
def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


@login_required
def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            reservation.user = request.user
            reservation.save()
            return redirect('booking_success')
    else:
        form = ReservationForm()
    return render(request, 'main/includes/reservation.html', {'form': form})




