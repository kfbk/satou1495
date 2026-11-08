from django import forms
from django.core.validators import RegexValidator

class GuessForm(forms.Form):
    number = forms.CharField(
        max_length=4,
        min_length=4,
        validators=[
            RegexValidator(r'^[0-9]{4}$', '半角数字4桁のみ入力してください。'),
        ],
        label='予想した数字'
    )