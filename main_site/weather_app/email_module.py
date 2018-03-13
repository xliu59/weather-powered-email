from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.core import mail
import os
import re


# param dictionary for email content customization
params = {
    'from_addr'            : "xiaoxiao.email.test@gmail.com",
    'good_weather_subject' : "It's nice out! Enjoy a discount on us.",
    'good_weather_image'   : 'good_weather.png',
    'bad_weather_subject'  : "Not so nice out? That's okay, enjoy a discount on us",
    'bad_weather_image'    : 'bad_weather.png',
    'default_subject'      : "Enjoy a discount on us",
    'default_image'        : 'default_weather.png',
    'body'                 : "Current weather in %s, %s : %s degress, %s.",
}


def create_email(data):
    """
    Create the email instance and use personalised email subject and body content.
    :param data: dictionary containing weather info
                 e.g. {"state": "NY", "city": "New_York", "weather": "Sunny", "temp": 51.2, "mean_temp": 51.2}
    :return: EmailMessage instance
    """
    weather_condition = get_weather_condition(data)
    # assemble the email content
    email = EmailMessage(
        subject=params[weather_condition + "_subject"],
        body=params['body'] % (data['city'].replace("_", " "), data['state'], data['temp'], data['weather']),
        from_email=params['from_addr'],
    )
    # attach a weather image
    image_name = params[weather_condition + "_image"]
    module_dir = os.path.dirname(__file__)
    image_path = os.path.join(module_dir + "/static/images/%s" % image_name)
    image_file = open(image_path, 'rb').read()
    email.attach(filename=image_name, content=image_file)
    return email


def get_weather_condition(data):
    """
    Criterion of determining weather condition. Used to change the subject of the email based on the weather.
    If it's nice outside, either sunny or 5 degrees warmer than the average temperature for that location at that
    time of year, the email's subject should be "It's nice out! Enjoy a discount on us."
    Or if's it's not so nice out, either precipitating or 5 degrees cooler than the average temperature,
    the subject should be "Not so nice out? That's okay, enjoy a discount on us."
    If the weather doesn't meet either of those conditions, it's an average weather day and
    the email subject should read simply "Enjoy a discount on us."

    :param data: dictionary containing weather info
                 e.g. {"state": "NY", "city": "New_York", "weather": "Sunny", "temp": 51.2, "mean_temp": 51.2}
    :return: string, be used as key for param dictionary to choose email subject
    """
    if re.match(r'.*sunny.*|.*clear.*', data['weather'].lower().strip()) or data['temp'] >= data['mean_temp'] + 5:
        return "good_weather"
    elif re.match(r'.*rain.*|.*snow.*', data['weather'].lower().strip()) or data['temp'] <= data['mean_temp'] - 5:
        return "bad_weather"
    else:
        return "default"


def send_email(cache):
    """
    Send email to each subscriber by using grouped City weather info,
    iterating through all subscribers of that city.
    Complexity of this step is O(number_of_total_subscribers)

    :param cache: dictionary {'state_name': {'city_name': {'email': emailMessage, 'to_list': ['xx@xx', ...] }}}
    :return:
    """
    with mail.get_connection() as connection:
        for state, s_data in cache.items():
            for city, c_data in s_data.items():
                email = c_data['email']
                to_list = c_data['to_list']
                for to in to_list:
                    try:
                        email.to = [to]
                        email.connection = connection
                        email.send(fail_silently=False)
                        print("%s ... sent" % to)
                    except Exception as e:
                        print("%s ... failed" % to)
                        print(e)

