1. Installation & App Configuration
Install via pip

bash
Copy
Edit
pip install django-simplemde
GitHub

Enable the app
In your settings.py:

python
Copy
Edit
INSTALLED_APPS = [
    # …
    'simplemde',
    # …
]
GitHub

Static files
If you serve static files from Django, ensure:

python
Copy
Edit
STATIC_URL = '/static/'
Then run:

bash
Copy
Edit
python manage.py collectstatic
2. Model Integration
Replace your standard TextField with SimpleMDEField so that any form or admin widget will render SimpleMDE automatically.

python
Copy
Edit
# models.py
from django.db import models
from simplemde.fields import SimpleMDEField

class Entry(models.Model):
    title   = models.CharField(max_length=250, verbose_name='Title')
    content = SimpleMDEField(verbose_name='Markdown content')

    def __str__(self):
        return self.title
The editor will store raw Markdown in the database. 
GitHub

3. Global Editor Options
You can tweak the SimpleMDE instance site-wide via settings.py:

python
Copy
Edit
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
Only static configurations are supported (no JS callbacks like previewRender). 
GitHub

4. Form & Admin Usage
4.1 ModelForm
When you use a ModelForm for your Entry model, django-simplemde will automatically apply the editor to the SimpleMDEField:

python
Copy
Edit
# forms.py
from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model  = Entry
        fields = ['title', 'content']
No extra widget declaration is needed! 
GitHub

4.2 Overriding on Existing TextField
If you have an existing TextField (not SimpleMDEField), you can still apply the editor by using the provided widget:

python
Copy
Edit
# forms.py
from django import forms
from simplemde.widgets import SimpleMDEEditor  # from django-wiki issue discussion
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ['content']
        widgets = {
            'content': SimpleMDEEditor(),
        }
GitHub

4.3 Django Admin
By default, any SimpleMDEField in your models will render appropriately in the admin. If you need to force the editor on all TextField instances:

python
Copy
Edit
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
5. Template Setup
Include CSS & JS
Add in your base template (or form template):

django
Copy
Edit
{% load static %}
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css">
<script src="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>
GitHub

Initialize on your textarea
If you need custom element targeting or additional JS tweaks:

html
Copy
Edit
<textarea id="id_content" name="content">{{ form.content.value }}</textarea>
<script>
  // Apply SimpleMDE to the textarea with id="id_content"
  new SimpleMDE({
    element: document.getElementById("id_content"),
    ...window.SIMPLEMDE_OPTIONS  // merges your Django settings
  });
</script>
GitHub

6. Handling Form Submission Issues
If you notice your form won’t submit (due to browser validation on the <textarea>), add the novalidate attribute to your <form> tag:

html
Copy
Edit
<form method="post" novalidate>
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>








 4. Install and set up django-cleanup
In terminal:

bash
Copy
Edit
pip install django-cleanup
Then add to INSTALLED_APPS:

python
Copy
Edit
INSTALLED_APPS = [
    ...
    'django_cleanup.apps.CleanupConfig',
]
This automatically deletes old files when new ones are uploaded or when media is deleted.

✅ 5. Show media and embed markdown in template
If you're using {{ post.body|markdown }} in your template, and the markdown includes:

markdown
Copy
Edit
![Alt text](/media/uploads/myimage.png)
<video controls><source src="/media/uploads/myvideo.mp4"></video>
…it will be rendered properly.

You can also display all uploaded media for a post like:

html
Copy
Edit
{% for file in post.media.all %}
  {% if file.file.url.endswith:".mp4" %}
    <video controls width="500">
        <source src="{{ file.file.url }}" type="video/mp4">
    </video>
  {% else %}
    <img src="{{ file.file.url }}" alt="media" style="max-width:100%;">
  {% endif %}
{% endfor %}