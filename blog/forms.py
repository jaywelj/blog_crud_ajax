from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ("title", "text")


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ["author", "text"]

	def __init__(self, *args, **kwargs):
		super(CommentForm, self).__init__(*args, **kwargs)
		self.fields['text'].widget.attrs.update({
			'class' : 'list-group-item w-75 border d-inline-block', 
			'placeholder': 'comment here..',
		})
		self.fields['author'].widget.attrs.update({
			'class' : 'list-group-item w-25 border d-inline-block', 
			'placeholder': 'Name',
		})
