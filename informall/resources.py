import csv
import json
import simplekml
from informall.models import *

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
        state_news = [news_data[state_name]['newspaper'], news_data[state_name]['tv'], news_data[state_name]['radio'], ]
        for type_of_news in state_news:
            for n in type_of_news:
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

def convert_to_kml(kml_sheet, type_of_org, descriptor_of_org):
    """
        type_of_org = library | news
        descriptor_of_org = public | academic | private | television | newspaper | radio
    """
    if type_of_org == 'library':
        all_orgs = list(Library.objects.all())
    elif type_of_org == 'news':
        all_orgs = list(News.objects.filter(newstype=descriptor_of_org))

    kml = simplekml.Kml()
    for org in all_orgs:
        kml.newpoint(name=org.name, description=descriptor_of_org, coords=[(org.longitude, org.latitude)])

    kml.save(kml_sheet)
