from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector

from .models import Post, Tag, Comment
from .forms import FilterForm, CommentForm, EmailPostForm




class PostView(LoginRequiredMixin, ListView):
    template_name = 'post.html'
    paginate_by = 3
    
    def get_queryset(self):
        query_set = Post.published.all()
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm
        return context


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,)
    form = CommentForm
    comments = post.comments.filter(active=True)
    # get all the tag ids in the current post and put them in a list 
    post_tags_ids = post.tags.values_list('id', flat=True)
    # find all the posts which have the same tag ids except the current post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # use annotate(for calculating and adding a field to the querryset like a loop) and as its calculator use Count(a django db class) to count the number of tags 
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'post_detail.html', {'post': post, 'form': form, 'comments': comments, 'similar_posts': similar_posts})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title', 'body', 'tags',)
    template_name = 'post_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Post has been updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Post has been deleted successfully!')
        return super().form_valid(form)


class PostNewView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'slug', 'body', 'tags',)
    template_name = 'post_new.html'
    success_url = reverse_lazy('post')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post has been added successfully! Admin will publish it ASAP!')
        return super().form_valid(form)


class TagNewView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ('title',)
    template_name = 'tag_new.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your tag has been added successfully!')
        return super().form_valid(form)


class TagFilterListView(ListView):
    model = Post
    template_name = "post.html"
    paginate_by = 3
    
    def get_queryset(self):
        '''Handle both tag links and tag filter form.'''
        tag_id = self.kwargs.get('pk')
        # Check if user clicked on any of the tag links
        if tag_id:
            tag = get_object_or_404(Tag, pk=tag_id)
            return tag.posts.order_by('-publish')
        
        tag_id = self.request.GET.get('filter', None)
        # Check if user used the filter form        
        if tag_id:
            tag = get_object_or_404(Tag, pk=tag_id)
            return tag.posts.order_by('-publish')
         
        # Bring all the posts if user clicked on ------- in the form
        return Post.objects.all()
           
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm
        return context


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            new_comment = Comment(comment=comment, author=request.user, post=post)
            new_comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form})



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject=subject, 
                      message=message, 
                      from_email=None,  # So it uses DEFAULT_FROM_EMAIL in the settings.py
                      recipient_list=[cd['to']])
            sent = True 
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 
                                                    'form': form, 
                                                    'sent': sent})
    

def post_search(request):
    form = FilterForm()
    query = None
    results = []

    query = request.GET.get('query')
    if query:
        print(query)
        # annotate combines the two field together
        # SearchVector converts text fields into a format that supports full-text search in PostgreSQL
        # filter finds the given words in the full-text
        results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
        print(results)
    return render(request, 'search_post_list.html', {'form': form, 'query': query, 'results': results})