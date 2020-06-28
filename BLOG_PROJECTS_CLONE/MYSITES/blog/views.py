from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment, UserRegisteration
from .forms import PostForm, CommentForm, UserForm, UserRegisterationForm
from django.contrib.auth.models import User

from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


def CreateRegisterView(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        register_form = UserRegisterationForm(data=request.POST)

        if user_form.is_valid() and register_form.is_valid():
            user1 = user_form.save()
            user1.set_password(user1.password)

            user1.save()

            register_user = register_form.save(commit=False)
            if 'profile_pic' in request.FILES:
                print("Found")
                register_user['profile_pic'] = request.FILES['profile_pic']

            register_user.save()
            registered = True
        else:
            print(user_form.errors, register_form.errors)
    else:
        user_form, register_form = UserForm(), UserRegisterationForm()
        context = {
            'registered': registered,
            'user_form': user_form,
            'register_form': UserRegisterationForm
        }
        return render(request, 'register', context)



#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required()
def change_password(request):
    u = User.objects.get(username='ravi2')
    u.set_password('267695')
    u.save()
    return redirect('login')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
