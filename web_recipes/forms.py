"""Recipe editing and validated image uploads."""

from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("name", "category", "image")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("Введите не менее трёх символов.")
        return name

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and hasattr(image, "content_type"):
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Фото не должно превышать 5 МБ.")
            if image.image.format not in {"JPEG", "PNG", "WEBP"}:
                raise forms.ValidationError("Разрешены JPEG, PNG и WebP.")
        return image
