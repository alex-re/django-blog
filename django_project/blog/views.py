from django.shortcuts import render
from django.http import HttpResponse  # if we have external html files we can comment this importing.

from .models import Post  # "." means models in this directory.
from django.views.generic import (  # ListView is class based view.
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.


# posts = [
#     {
#         'author':'khodam',
#         'title':'Blog post 1',
#         'content':'First post content',
#         'date_posted':'Agust 27, 2018'
#     },
#     {
#         'author':'chalghoos',
#         'title':'Blog post 2',
#         'content':'Second post content',
#         'date_posted':'Agust 30, 2020'
#     }
# ]


def home(request):
    context = {
        # 'posts':posts
        'posts':Post.objects.all()
    }

    # return HttpResponse("<h1> Blog Home </h1>")
    return render(request, 'blog/home.html', context)  # ~/django/django_project/blog/templates/blog/home.html


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # "-" for reverse it (newer in top)


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # those has to be on the left
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    # return HttpResponse("<h1> Blog About </h1>")
    return render(request, 'blog/about.html', {'title':'About'})

