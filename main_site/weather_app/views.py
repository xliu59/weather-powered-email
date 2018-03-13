from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Subscriber, City
from .forms import RegisterForm


def register_email(request):
    """
    Render the register page, differently response to GET and POST. User Input validation applied
    :param request:
    :return:
    """
    # POST to this function when user submit form
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)

        # check if input values are valid, .clean() method will be called
        if form.is_valid():
            # processing the data in form.cleaned_data
            email = form.cleaned_data.get('email')
            city_pk = form.cleaned_data.get('location')
            city = City.objects.get(pk=city_pk)
            new_subscriber = Subscriber(email=email, city=city, status='active')
            # save new subscriber instance
            new_subscriber.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('weather_app:confirm'))

    # GET (or else) to this function when request the empty form at the first time
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'css_src': 'css/style.css',
        'title': 'Weather Powered Email',
    }

    return render(request, 'weather_app/register.html', context)


def confirm(request):
    """
    Render the confirm page
    :param request:
    :return:
    """
    return render(request, 'weather_app/confirm.html', {
        'img_src': 'images/check.png',
        'img_alt': "success",
        'h1': "Success!",
        'h2': "Your email has successfully registered! Thank you!",
        'home': 'register',
        'css_src': 'css/style.css',
    })
