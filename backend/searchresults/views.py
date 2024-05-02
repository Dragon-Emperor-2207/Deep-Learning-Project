from django.http import JsonResponse
from imdb import Cinemagoer
import requests
from summarizer import main

ia = Cinemagoer()
def search(request):
    param_value = request.GET.get('data')
    movies = title_id(param_value)
    return JsonResponse(movies)

def title_id(name):
    url = "https://imdb8.p.rapidapi.com/auto-complete"
    querystring = {"q":name}
    headers = {
	    "X-RapidAPI-Key":"81f06e6ff8msh412817c08531a45p158f86jsn1050cfdaf157",
	    "X-RapidAPI-Host":"imdb8.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    res=response.json()
    d = {}
    for i in res['d']:
        try:
            if 'imageUrl' in i['i'].keys():
                d[i['l']] =  { 'imageUrl': i['i']['imageUrl'], 'id': i['id']}
            else:
                d[i['l']] = {'id': i['id']}
        except:
            print("Key error")
    return d

def reviews(id):
    url = "https://imdb8.p.rapidapi.com/title/get-user-reviews"
    querystring = {"tconst":id}
    headers = {
	    "X-RapidAPI-Key":"81f06e6ff8msh412817c08531a45p158f86jsn1050cfdaf157",
	    "X-RapidAPI-Host":"imdb8.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    res=response.json()
    for i in range(len(res["reviews"])):
        #print(res["reviews"][i])
        if "authorRating" not in res["reviews"][i].keys():
            with open('neutral_reviews.txt', 'a', encoding='utf-8') as file:
                x = ':$' + res['reviews'][i]['reviewText']
                file.write(x)
        elif(res["reviews"][i]["authorRating"]>=8):
            with open('good_reviews.txt', 'a', encoding='utf-8') as file:
                x = ':$' + res['reviews'][i]['reviewText']
                file.write(x)
        elif(res["reviews"][i]["authorRating"]<=7 and res["reviews"][i]["authorRating"]>=6):
            with open('neutral_reviews.txt', 'a', encoding='utf-8') as file:
                x = ':$' + res['reviews'][i]['reviewText']
                file.write(x)
        elif(res["reviews"][i]["authorRating"]<6):
            with open('bad_reviews.txt', 'a', encoding='utf-8') as file:
                x = ':$' + res['reviews'][i]['reviewText']
                file.write(x)

def summary(request):
    id = request.GET.get('data')
    return JsonResponse(main(id))