from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import AddCommentForm
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize


from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated 

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

import datetime
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http import JsonResponse

year = datetime.datetime.now().year

def home(request):
    posts = Post.objects.all()
    context = { 'posts': posts , 'title': 'Home', 'date': year}
    return render(request, "blog/home.html", context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostLikeAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request, pk=None, format=None):
        pk = self.kwargs.get('pk')
        print(pk)
        print(self.request.user)
        post = get_object_or_404(Post, pk=pk)
        url_ = post.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False

        token, created = Token.objects.get_or_create(user=user)
        print(token)
        
        # user = authenticate(username=user.username, password=user.password)
        if(user.is_authenticated):
            if(user in post.likes.all()):
                liked = False
                post.likes.remove(user)
            else:
                liked  =True
                post.likes.add(user)
            updated = True
        data = {
            'updated': updated,
            'liked': liked,
            'count': post.likes.count(),
            'postid':post.id
        }
        return Response(data)
    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # get the post form the database
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        # get the list of comments related to this post
        context['comment_list'] = post.comment_set.all()
        print(context['comment_list'])
        context['form'] = AddCommentForm()
        return context

    


def addcomment(request):
    if( request.is_ajax() ):
        # print(request.POST.get('content'))
        # print(request.POST.get('id'))
        content = request.POST.get('content')
        id = request.POST.get('id')
        post = Post.objects.get(pk=id)
        # print(post.pk)
        print(request.user)
        comment = Comment.objects.create(
            content=content,
            on_post_id=post.pk,
            author=request.user
        )
        print(comment.pk)
        data = dict()
        # comments_final = list()
        data['message'] = 'comment has been added successfully'
        data['post_id'] = id
        data['comment_id'] = comment.pk
        return JsonResponse(data)
    
    return HttpResponse('')


def commentlist(request):
    if(request.method == 'GET'):
        print("---------",request.GET.get('post_id'))
        id = request.GET.get('post_id')
        comment_id = request.GET.get('comment_id')
        print(",-------,",comment_id )
        post = Post.objects.get(pk=id)
        print(post)
        comments = list(post.comment_set.all().values())
        print(comments)
        print(type(comment_id))
        comment1 = Comment.objects.get(id=comment_id)
        print('======||======',comment1.author.profile.image.url)
        comments_final = list()
        for comment in comments:
            if( comment['id'] == int(comment_id)  ):
                print('true')
                com = {
                    'id': comment['id'],
                    'content': comment['content'], 
                    'on_post': comment1.author.profile.image.url, 
                    'author': User.objects.get(pk=comment['author_id']).username
                }
                # print(com)
                print(com['on_post'])
                comments_final.append(com)
        # print(comments_final)
        data = dict()
        data['comment_list'] = comments_final
        data['comment_count'] = len(comments)
        return JsonResponse(data)
    return HttpResponse('')
   
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    # success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def about(request): 
    context = { 'title': 'About' , 'date': year}    
    return render(request, "blog/about.html", context)

