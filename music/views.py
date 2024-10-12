from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
import requests
import base64


# client_id = 'your_client_id'
# client_secret = 'your_client_secret'
# credentials = f"{'4175714326124471a9a3ed938fc4da79'}:{'dc8df16fed95440a9c423bdf9e07abdc'}"
# base64_credentials = base64.b64encode(credentials.encode()).decode()


# token_url = "https://accounts.spotify.com/api/token"
# headers = {
#     "Authorization": f"Basic {base64_credentials}",
#     "Content-Type": "application/x-www-form-urlencoded"
# }
# data = {
#     "grant_type": "client_credentials"
# }

# response = requests.post(token_url, headers=headers, data=data)
# access_token = response.json().get("access_token")

# print(f"Access Token: {access_token}")

# #this worked properly bro this gave me an accestoken :)





# import requests
# import base64  # Don't forget to import base64
# from django.shortcuts import render

# def spotify_login(request):
#     # Step 1: Obtain the Access Token
#     client_id = 'your_client_id'
#     client_secret = 'your_client_secret'
#     credentials = f"{'4175714326124471a9a3ed938fc4da79'}:{'dc8df16fed95440a9c423bdf9e07abdc'}"
#     base64_credentials = base64.b64encode(credentials.encode()).decode()

#     token_url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": f"Basic {base64_credentials}",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {
#         "grant_type": "client_credentials"
#     }

#     response = requests.post(token_url, headers=headers, data=data)
#     access_token = response.json().get("access_token")
    
#     # Debug: Print access token
#     print(f"Access Token: {access_token}")

#     if not access_token:
#         return render(request, 'error.html', {'message': 'Could not obtain access token.'})

#     # Step 2: Use the Access Token to Get Top Artists
#     artists_url = artists_url = "https://api.spotify.com/v1/artists?ids=<comma-separated-artist-ids>"

#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }

#     artist_response = requests.get(artists_url, headers=headers)

#     # Debug: Print response status and data
#     print(f"Artist Response Status: {artist_response.status_code}")
#     print(f"Artist Response Data: {artist_response.json()}")

#     if artist_response.status_code != 200:
#         return render(request, 'error.html', {'message': 'Could not fetch artist information.'})

#     artists = artist_response.json().get('items', [])

#     # Debug: Print the artists
#     print(f"Artists: {artists}")

#     # Step 3: Render the artists in the template
#     return render(request, 'music/artists.html', {'artists': artists})




# Create your views here.
def top_artists():
    url = "https://spotify-scraper.p. rapidapi.com/v1/chart/artists/top"
    headers = {
        "X-RapidAPI-Key": "02912db996msh068b089c778126bp13a9d9jsn380afeb7d573",
        "X-RapidAPI-Host": "spotify-scraper.p. rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    artists_info = []

    if 'artists' in response_data:

        for artists in response_data['artists']:
            name = artists.get('name', 'No Name')
            avatar_url = artists.get('visuals', {}).get('avatar', [{}])[0].get('url', 'No URL')
            artist_id = artists.get('id', 'No ID')
            artists_info.append((name, avatar_url, artist_id))
    
    return artists_info

def top_tracks():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/tracks/top"
    
    headers = {
        "X-RapidAPI-Key": "02912db996msh068b089c778126bp13a9d9jsn380afeb7d573",
        "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    track_details = []
    
    if 'tracks' in data:
        shortened_data = data['tracks'][:18]
        # id, name, artist, cover url
        for track in shortened_data:
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name'] if track['artists'] else None
            cover_url = track['album']['cover'][0]['url'] if track['album']['cover'] else None
            
            track_details.append({
                'id': track_id,
                'name': track_name,
                'artist': artist_name,
                'cover_url': cover_url
            })
    else:
        print('Track not found in response')
    
    return track_details

def music (request, pk):
    return render(request, 'music.html')


@login_required(login_url='login')
def index(request):

    # artists_info = top_artists()
    # top_track_list = top_tracks()
    # print(top_track_list)

    # context = {
    #     'artists_info' : artists_info,
    # }

    return render(request, 'index.html', )

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            #log user in
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()


                #log user in
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')

