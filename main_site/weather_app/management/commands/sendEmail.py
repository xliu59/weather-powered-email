from django.core.management.base import BaseCommand, CommandError
from ...weather_module import get_weather
from ...email_module import create_email, send_email
from ...models import Subscriber


class Command(BaseCommand):
    help = "Send email to all subscribers"

    def handle(self, *args, **optinons):
        """ Handle the "sendEmail" command """
        try:
            print("sending email now...")
            active_users = Subscriber.objects.filter(status="active")
            cache = {}      # use cache to save requested city
            for user in active_users:
                city = user.city.city_name
                state = user.city.state_abbr

                if state not in cache or city not in cache[state]:
                    weather = get_weather(state, city)
                    email = create_email(weather)
                    if state not in cache:
                        cache[state] = {}
                    cache[state][city] = {'email': email, 'to_list': []}
                # save new city to cache
                cache[state][city]['to_list'].append(user.email)
            send_email(cache)

        except Exception as e:
            raise CommandError(e)

        # OPTIONAL: save history temperature data (from cache) to db,
        #           good for performance on same-date repeating request

