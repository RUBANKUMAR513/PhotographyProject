# your_app/forms.py

from django import forms
from .models import BabyPropsImage

class BabyPropsImageAdminForm(forms.ModelForm):
    class Meta:
        model = BabyPropsImage
        fields = ['gallery', 'image', 'description']  # Include description if you want to allow editing

    def clean(self):
        cleaned_data = super().clean()
        gallery = cleaned_data.get('gallery')

        # Check if the form is being used to create a new image instance
        if gallery and not self.instance.pk:  # This means it's a new instance
            if gallery.images.count() >= 5:
                raise forms.ValidationError('You can only add up to 5 images per Baby Props Gallery.')

        return cleaned_data

