# Django Blogging System with REST, GraphQL, Markdown & Media Support

A robust and modern blogging platform built with Django, featuring REST and GraphQL APIs, Markdown support with image/video embedding, a recommendation system, email backend, comment system, and automatic media cleanup.

---

## Features

- **Blog Posts & Comments**
  - Create, update, and manage posts and comments.
  - Nested comment support via DRF and GraphQL.

- **API Support**
  -  **REST API** with Django REST Framework
  -  **GraphQL API** using Graphene-Django
  -  Token-based authentication

- **Markdown Editor**
  - SimpleMDE Markdown editor for rich-text content
  - Supports image and video embedding

- **Media Management**
  - Upload and display media (images/videos)
  - Automatic media cleanup with `django-cleanup`

- **Recommendation System**
  - Suggest related posts dynamically

- **Email Notifications**
  - Notify users on new posts or comments

---

## 🛠️ Tech Stack

- **Backend:** Django, DRF, Graphene-Django  
- **Database:** PostgreSQL / SQLite  
- **Auth:** Token-based authentication  
- **Editor:** SimpleMDE  
- **File Management:** django-cleanup  
- **Media Support:** Markdown image/video embedding

---

##  Installation

```bash
git clone https://github.com/yourusername/blogging-platform.git
cd blogging-platform
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

##  App Configuration
```python
# settings.py

INSTALLED_APPS = [
    ...
    'simplemde',
    'django_cleanup.apps.CleanupConfig',
    ...
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Markdown with SimpleMDE
1. Model Integration
```python
# models.py
from django.db import models
from simplemde.fields import SimpleMDEField

class Entry(models.Model):
    title   = models.CharField(max_length=250, verbose_name='Title')
    content = SimpleMDEField(verbose_name='Markdown content')

    def __str__(self):
        return self.title
```

2. Global Editor Settings
```python
# settings.py

SIMPLEMDE_OPTIONS = {
    'placeholder': 'Start writing in Markdown…',
    'status': False,            # hide status bar
    'autosave': {
        'enabled': True,
        'delay': 1000,         # milliseconds
    },
    # …any other SimpleMDE config keys
}
```

3. ModelForm & Widget Override
```python
# forms.py
from django import forms
from .models import Entry
from simplemde.widgets import SimpleMDEEditor

class EntryForm(forms.ModelForm):
    class Meta:
        model  = Entry
        fields = ['title', 'content']
```
```python
# For existing TextField override
# forms.py
from django import forms
from simplemde.widgets import SimpleMDEEditor
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ['content']
        widgets = {
            'content': SimpleMDEEditor(),
        }
```

4. Django Admin Integration
```python
# admin.py
from django.contrib import admin
from simplemde.widgets import SimpleMDEEditor
from django.db import models
from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': SimpleMDEEditor},
    }
```

## Media Upload & Display
Markdown Embedding in Content
```
![Image Alt](/media/uploads/image.png)

<video controls>
  <source src="/media/uploads/video.mp4" type="video/mp4">
</video>
```

Template Display Example
```
{% for file in post.media.all %}
  {% if file.file.url.endswith:".mp4" %}
    <video controls width="500">
      <source src="{{ file.file.url }}" type="video/mp4">
    </video>
  {% else %}
    <img src="{{ file.file.url }}" alt="media" style="max-width:100%;">
  {% endif %}
{% endfor %}
```

REST API Authentication
```
POST /api/token-auth/
Content-Type: application/json

{
  "username": "yourusername",
  "password": "yourpassword"
}
```

Use returned token:
```
Authorization: Token your_token
```

GraphQL Example Query
```
query {
  allPosts {
    title
    content
    author {
      username
    }
    comments {
      content
      createdAt
    }
  }
}
```
Visit /graphql/ to explore via GraphiQL.


