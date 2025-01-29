from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.http import Http404

from .models import Post
from .forms import PostForm

from apps.profiles.models import Profile
from apps.comments.models import Comment
from apps.comments.forms import CommentForm

from utilities.authenticators import when_logged_inc

# Create your views here.
class BlogView(ListView):
    paginate_by = 2
    model = Post
    
    def get(self, request, *args, **kwargs):
        try:
            page = abs(int(request.GET['page']))
            size = abs(int(request.GET['size']))
            amount = int(Post.objects.count() / size)
            amount, divrest = divmod(Post.objects.count(), size)
            amount = amount + 1 if divrest else amount
            if page == 0 or page > amount:
                raise Exception('Only one page')
            context = {
                'objects' : Post.objects.all()[page * size - size : page * size],
                'page' : page,
                'size' : size,
                'amount' : amount,
                'has_previous': page != 1,
                'has_next' : page != amount,
                'previous_page_number' : page - 1,
                'next_page_number' : page + 1,
            }
        except:
            page = 1
            amount, divrest = divmod(Post.objects.count(), 10)
            amount = amount + 1 if divrest else amount
            context = {
                'objects' : Post.objects.all()[:10],
                'page' : page,
                'amount' : int(Post.objects.count() / 10) + 1,
                'has_previous': False,
                'has_next' : page != amount,
                'next_page_number' : page + 1
            }

        return render(request, 'blog/index.html', context)

class PostCreateView(View):

    @when_logged_inc
    def get(self, request, form=None, *args, **kwargs):
        form = form or PostForm()
        context = {
            'post_form' : form
        }
        return render(request, 'blog/create.html', context)
    
    @when_logged_inc
    def post(self, request, form=None, *args, **kwargs):
        create_flag = form == None
        form = form or PostForm(request.POST)
        if form.is_valid():
            print('VALID:', request.POST)
            profile = get_object_or_404(Profile, user=request.user)
            post = form.save(profile, create=create_flag)
            return redirect(f'/blog/{post.slug}/')
        context = {
            'post_form' : form
        }
        return render(request, 'blog/create.html', context)
    

class PostView(View):

    def get(self, request, slug, *args, **kwargs):
        obj = get_object_or_404(Post, slug=slug)
        recent_posts = [(p.title, p.get_published_date(), p.slug) for p in Post.objects.filter(author=obj.author)[:3]]
        comment_form = CommentForm()
        #comment_form.parent.widget.attrs['value'] =obj.root_comment.id
        context = {
            'obj' : obj,
            'recent_posts' : recent_posts,
            'comment_form' : comment_form,
        }
        return render(request, 'blog/detail.html', context)
    
    def post(self, request, slug, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, user=request.user)
            post = get_object_or_404(Post, slug=slug)
            comment = form.save(profile)
            parentid = int(form.cleaned_data['parent'])
            parentid = parentid if parentid != -1 else post.root_comment.id
            parent = get_object_or_404(Comment, id=parentid)
            parent.children_comments.add(comment)
            post.root_comment = post.root_comment or comment
            #post.comments.add(comment)
            #post.save()
        return redirect('./#CommentSection')

class PostDeleteView(View):

    @when_logged_inc
    def post(self, request, slug, *args, **kwargs):
        obj = get_object_or_404(Post, slug=slug)
        if obj.author.user == request.user:
            if obj.root_comment:
                obj.root_comment.delete_comment()
            obj.delete()
        return redirect('/blog/')
    
    @when_logged_inc
    def get(self, request, slug, *args, **kwargs):
        raise Http404('Ta strona nie istnieje')

class PostEditView(PostCreateView):
    
    @when_logged_inc
    def get(self, request, slug, *args, **kwargs):
        obj = get_object_or_404(Post, slug=slug)
        form = PostForm(instance=obj)
        return super().get(request, form=form)
    
    @when_logged_inc
    def post(self, request, slug, *args, **kwargs):
        obj = get_object_or_404(Post, slug=slug)
        print(request.POST)
        form = PostForm(request.POST or None, instance=obj)
        super().post(request, form=form)
        return redirect(f'/blog/{slug}/')