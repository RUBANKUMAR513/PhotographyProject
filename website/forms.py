from django import forms
from .models import BabyPropsImage,OurServicesImage
from django.core.exceptions import ValidationError


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


class OurServicesImageAdminForm(forms.ModelForm):
    class Meta:
        model = OurServicesImage
        fields = ['services', 'image', 'description']  # Include description if you want to allow editing

    def clean(self):
        cleaned_data = super().clean()
        services = cleaned_data.get('services')

        # Check if the form is being used to create a new image instance
        if services and not self.instance.pk:  # This means it's a new instance
            if services.images.count() >= 10:
                raise forms.ValidationError('You can only add up to 10 images per services.')
        return cleaned_data


