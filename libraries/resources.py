import csv
import json
from .models import *

def get_libraries(libraries_csv):
    with open(libraries_csv, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            state, created = State.objects.get_or_create(name=row['STABR'])
            state.save()
            try:
                library, created= Library.objects.get_or_create(
                    name=row['LIBNAME'],
                    state=state,
                    latitude=row['LATITUDE'],
                    longitude=row['LONGITUD'],)
                library.save()
            except:
                print("ERROR!",row['LIBNAME'])
                pass

def get_news(news_json):
    json_data = open(news_json)
    news_data = json.load(json_data)
    for state_name in news_data:
        state, created = State.objects.get_or_create(name=state_name)
        state.save()
        all_news = news_data[state_name]['newspaper']
        for n in all_news:
            try:
                news, created = News.objects.get_or_create(
                    newstype=n['media-class'],
                    name=n['name'],
                    state=state,
                    longitude=n['city-county-long'],
                    latitude=n['city-county-lat'],)
                news.save()
            except:
                print("ERROR!", n)
                pass
