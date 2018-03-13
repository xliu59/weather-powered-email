from django import forms
from .models import City, Subscriber
import re
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    email = forms.CharField(
        label="Email Address",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'text_input'})
    )
    location = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        cities = City.objects.filter(pk__lt=101).order_by("pk").values_list("pk", "city_name")
        choices = tuple([(u'', "Where do you live?")] + list(cities))

        self.fields['location'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': 'choice_input'}),
        )

    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        if not email or len(email) == 0:
            raise ValidationError("email cannot be empty!")
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            raise ValidationError("invalid email format!")
        if Subscriber.objects.filter(email=email).exists():
            raise ValidationError("email already exists!")
        return email

    def clean_location(self):
        location_id = self.cleaned_data.get('location')
        if not location_id:
            raise ValidationError("location cannot be empty!")
        if not location_id.isdigit():
            print("location=", type(location_id))
            raise ValidationError("invalid location!")
        if location_id == -1:
            raise ValidationError("Please choose a location!")
        if not City.objects.filter(pk=location_id).exists():
            raise ValidationError("unrecognized location!")
        return location_id