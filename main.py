from yandex_music import Client
import time
import sqlite3
import config


# инициализация базы данных
connetion = sqlite3.connect('tracks.db')
cursor = connetion.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tracks (
                  id INTEGER PRIMARY KEY,
                  artist TEXT,
                  title TEXT
              )
''')
connetion.close()


class User:
    def __init__(self, uid) -> None:
        self.uid = uid
        self.tracklist = client.users_likes_tracks(user_id=self.uid)
        self.tracklist_proceseed = []

    def add_track_db(self, track_id, artist, title):
        # добавляет информацию о треке в БД
        connetion = sqlite3.connect('tracks.db')
        cursor = connetion.cursor()
        cursor.execute('''INSERT or IGNORE INTO tracks (id, artist, title)
                          VALUES (?, ?, ?)''', (track_id, artist, title))
        connetion.commit()
        connetion.close()

    def get_tracklist(self) -> []:
        # Получает треклист полсьователя по его ID
        # Отображает процесс обработки данных
        # TODO вынести прогресс бар в отдельное место
        tracks_count = len(self.tracklist)
        for i, track in enumerate(self.tracklist, 1):
            start_time = time.time()

            track_id = track.fetch_track()['id']
            artist = track.fetch_track()['artists'][0]['name']
            title = track.fetch_track()['title']
            self.tracklist_proceseed.append(track_id)

            end_time = time.time()
            time_elapsed = end_time - start_time
            time_left = time_elapsed*(tracks_count-i)

            self.add_track_db(track_id, artist, title)

            print(f'{i}/{tracks_count} {round(time_left, 3)} s', end='\r')
        print()


client = Client(config.ACCESS_TOKEN)
client.init()

first_user = User('polar.christin')
second_user = User('lovehate16605')

first_user.get_tracklist()
second_user.get_tracklist()

common_tracks = []

for track in first_user.tracklist_proceseed:
    if track in second_user.tracklist_proceseed:
        common_tracks.append(track)

result = []

# выбираем треки по ID из БД
connetion = sqlite3.connect('tracks.db')
cursor = connetion.cursor()
for track in common_tracks:
    print(track)
    cursor.execute('SELECT artist, title FROM tracks WHERE id = ?', (track,))
    result.append(cursor.fetchall())
connetion.close()

for track in result:
    print(f'{track[0][0]} - {track[0][1]}')
