from django import forms
from .models import FoodRequest


class FoodRequestForm(forms.ModelForm):

    class Meta:
        model = FoodRequest
        fields = ['request_text', 'requested_time']

        widgets = {
            'requested_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),
        }