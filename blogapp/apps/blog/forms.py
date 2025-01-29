from django import forms
from datetime import datetime
from django_ckeditor_5.widgets import CKEditor5Widget


from .models import Post
from apps.comments.models import Comment

class CustomCKEditorWidget(CKEditor5Widget):
    def render(self, name, value, attrs=None, renderer=None):
        # Call the parent class's render method
        rendered = super().render(name, value, attrs, renderer)
        
        # # Customize the attributes
        # new_attrs = {'class': 'my-custom-class', 'style': 'display: block;'}
        # rendered = rendered.replace('class="django-ckeditor-widget"', f'class="django-ckeditor-widget {new_attrs["class"]}"')
        # rendered = rendered.replace('style="display: inline-block;"', f'style="{new_attrs["style"]}"')

        return rendered

class PostForm(forms.ModelForm):
    title    = forms.CharField(label='Tytuł', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtitle = forms.CharField(label='Podtytuł', widget=forms.TextInput(attrs={'class': 'form-control'}))
    body     = forms.CharField(label='', widget=CustomCKEditorWidget())
    #body     = RichTextFormField(label='', )
    #body     = forms.CharField(label='Treść', widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100%;'}))

    class Meta:
        model = Post
        fields = (
            'title',
            'subtitle',
            # 'body',
        )

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

    def save(self, author, create=False, commit=True):
        print('saving')
        print(self.data)
        post = super(PostForm, self).save(commit=False)
        post.author = author
        post.body = self.data['body']
        if create:
            post.publish_date = datetime.now()
            print('lol1')
            post.root_comment = Comment.objects.create()
            print('lol2')
        else:
            post.date_modified = datetime.now()

        if create or post.slug == None:
            post.slug = post.get_slug()

        if commit:
            post.save()
            
        return post