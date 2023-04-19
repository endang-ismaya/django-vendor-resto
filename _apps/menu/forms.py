from django import forms

from _apps.menu.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("category_name", "description")
