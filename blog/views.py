from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib import messages

from .models import Post, Tag, Comment
from .forms import FilterForm, CommentForm



# Create your views here.
class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post.html'
    paginate_by = 3
    ordering = '-date'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


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
    fields = ('title', 'body', 'tags',)
    template_name = 'post_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post has been added successfully!')
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
        '''Handle both tag links and filter form.'''
        tag_id = self.kwargs.get('pk')
        # Check if user clicked on any of the tag links
        if tag_id:
            tag = get_object_or_404(Tag, pk=tag_id)
            return tag.posts.order_by('-date')
        
        tag_id = self.request.GET.get('filter', None)
        # Check if user used the filter form        
        if tag_id:
            tag = get_object_or_404(Tag, pk=tag_id)
            return tag.posts.order_by('-date')
         
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
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form})

