import telebot
from telebot import types
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
from youtubesearchpython import VideosSearch



bot = telebot.TeleBot('6600134179:AAGUt1bvS_iuKJUYvZKCZfIDfX6711CaesI')
client_id = 'ec8ffbd858d04a57ba92e8bad3e618cf'
client_secret = '4edf9dae8e784272b4c3bdd43e46ec47'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
playlist_id = 'https://open.spotify.com/playlist/1oD0Txed1OzOFlno8kpWNz?si=fa1a416fcc124578'

all_tracks = []
results = sp.playlist_tracks(playlist_id, limit=100)
while results['next']:
    results = sp.next(results)
    if results:
        all_tracks.extend(results['items'])
    else:
        break



artists = ''

def youtube_search(search_query):
    videos_search = VideosSearch(search_query, limit=1)
    first_video = videos_search.result()['result'][0]
    video_link = first_video['link']
    combined_message = f"{search_query}\n{video_link}"
    return combined_message


@bot.message_handler(commands=['start'])
def start(message):
    image_url = 'https://sun9-28.userapi.com/impg/wErJ_ftLkgAx2Z8KYq1oIkkpk1Zbe0pFEYXvsw/3mBaQp-0cj8.jpg?size=828x817&quality=95&sign=67c2bca7b26990ea5137cf96094e9171&type=album'
    bot.send_photo(message.chat.id, image_url)
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Хотю музяки')
    keyboard.add(button1)

    bot.send_message(message.chat.id, 'Привет! Это бот для рекоммендации музыки. Музяки хочешь?', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Хотю музяки')
def music_recommendation(message):
    global artists
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton('Хотю музяки')
    button2 = types.KeyboardButton('Еще от этого артиста')
    keyboard.add(button1, button2)

    random_track = random.choice(all_tracks)['track']
    artists = ', '.join([artist['name'] for artist in random_track['artists']])
    song = random_track['name']
    search_query = artists + " - " + song

    bot.send_message(message.chat.id, youtube_search(search_query), reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Еще от этого артиста')
def more_from_artist(message):
    global artists
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton('Хотю музяки')
    button2 = types.KeyboardButton('Еще от этого артиста')
    keyboard.add(button1, button2)

    artist_name = artists.split(',')[0]
    results = sp.search(q=artist_name, type='artist')
    artist_id = results['artists']['items'][0]['id']
    results = sp.artist_top_tracks(artist_id)
    all_tracks = []
    for track in results['tracks']:
        all_tracks.append(track['uri'])
    random_track_uri = random.choice(all_tracks)
    random_track_info = sp.track(random_track_uri)
    search_query = random_track_info['artists'][0]['name'] + " - " + random_track_info['name']

    bot.send_message(message.chat.id, youtube_search(search_query), reply_markup=keyboard)
    pass


bot.polling()