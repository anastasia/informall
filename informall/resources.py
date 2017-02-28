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
        all_orgs = list(Library.objects.all(institution_type=descriptor_of_org))
    elif type_of_org == 'news':
        all_orgs = list(News.objects.filter(newstype=descriptor_of_org))

    count = 0
    kml = simplekml.Kml()
    name = kml_sheet.split('.kml')[0]
    for idx,org in enumerate(all_orgs):
        kml.newpoint(name=org.name, description=descriptor_of_org, coords=[(org.longitude, org.latitude)])
        if idx % 1000 == 0:
            count += 1
            kml_sheet = name + str(count) + '.kml'
            f = open(kml_sheet,'w')
            f.close()
            # write kml to kml_sheet
            kml.save(kml_sheet)
            kml = simplekml.Kml()
    count += 1
    kml_sheet = name + str(count) + '.kml'
    f = open(kml_sheet,'w')
    f.close()
    kml.save(kml_sheet)

def library_pk_csv(csvname):
    fieldnames = ['id', 'library']
    libraries = list(Library.objects.all())
    with open(csvname, 'rb+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for library in libraries:
            writer.writerow({'id':library.pk, 'library':library.name})

def parse_libguides_db(csvname):
    fieldnames = ["Library Name", "Database", "Database URL", "Database Description"]
    with open(csvname, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            resource_name = unicode(row["Database"], "utf-8")
            library_name = unicode(row["Library Name"], "utf-8")
            if library_name != "Library Name":
                # omit public schools (journalists won't have access)
                if not "public school" in library_name.lower():
                    try:
                        library, created = Library.objects.get_or_create(name=library_name.upper())
                        resource, created = Resource.objects.get_or_create(name=resource_name)
                        library.institution_type = 'academic'
                        resource.description = row["Database Description"]
                        resource.website = row["Database URL"]
                        resource.save()
                        library.resources.add(resource)
                        library.save()
                    except Exception as e:
                        pass

def get_university_coordinates(csvname):
    with open(csvname, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            uniname = row["INSTNM"]
            if 'California-Berkeley' in uniname:
                uniname = 'UC BERKELEY'

            uniname = unicode(uniname, errors='ignore')
            library, just_created = Library.objects.get_or_create(name=uniname.upper())

            try:
                library.longitude = float(row["LONGITUD"])
                library.latitude = float(row["LATITUDE"])
                library.institution_type = "academic"
            except:
                pass
            library.website = row["WEBADDR"]
            library.save()
