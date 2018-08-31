import json
import spotipy
import spotipy.util as util
import os
import itertools


scope = 'user-library-read'

def set_env_vars():

    with open('access.json') as f:
        data = json.load(f)

    os.environ["SPOTIPY_CLIENT_ID"] = data["SPOTIPY_CLIENT_ID"]
    os.environ["SPOTIPY_CLIENT_SECRET"] = data["SPOTIPY_CLIENT_SECRET"]
    os.environ["SPOTIPY_REDIRECT_URI"] = data["SPOTIPY_REDIRECT_URI"]

songs = []
artists = []
added = []
colaborations = []
albums = []

def add_track(track):

    for artist in track["artists"]:
        new_colaborations = [(artist["name"].lower(), track["album"]["name"].lower()),
                             (track["album"]["name"].lower(), track["name"].lower())]
        colaborations.extend(list(set(new_colaborations) - set(colaborations)))
        if artist["name"].lower() not in added:
            artists.append({"name": artist["name"].lower(), "popularity": int(track["popularity"]),"type": "artist"})
            added.append(artist['name'].lower())
    if (len(added) > 1):
        links = list(itertools.combinations(added, 2))
        colaborations.extend(list(set(links) - set(colaborations)))

    # dict["artists"] = track_artists
    album = { "name": track["album"]["name"].lower(), "images":track['album']['images'][0]['url'],"type": "album"}
    if album not in albums: albums.append(album)

    song = {"name": track["name"].lower(), "popularity": int(track["popularity"]), "type": "track"}
    if not song in songs:
        songs.append(song)

def process_playlists(sp, playlists):
    i = 1
    banned_playlist = []
    for playlist in playlists['items']:
        if i == 2:
            break
        print(playlist["name"])
        name = playlist["name"]
        if name not in banned_playlist:
            if playlist['owner']['id'] == sp.current_user()["id"]:
                print("\tProcesando")
                results = sp.user_playlist(sp.current_user()["id"], playlist['id'],
                                           fields="tracks,next")
                tracks = results['tracks']
                for track in tracks["items"]: add_track(track["track"])
                while tracks['next']:
                    tracks = sp.next(tracks)
                    for track in tracks["items"]:
                        add_track(track["track"]);

                i = i + 1

def spotipy_call(username):

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth = token)
        playlists = sp.user_playlists(sp.current_user()["id"])
        process_playlists(sp, playlists)
        """
        while playlists["next"]:
            playlists = sp.next(playlists)
            process_playlists(sp, playlists)
        """

    else:
        print("Can't get token for", username)


def write_output():
    output = {
        "directed": False,
        "graph": {},
        "nodes": songs + artists + albums#,
        #"links": [ {"source": {"name": source }, "target": {"name": target }} for source, target in colaborations ]
    }
    source = ""
    target = None
    links = []
    for (sour, tar) in colaborations:
        for (index, d) in enumerate(output["nodes"]):
            if d["name"] == sour:
                source = index
            elif d["name"] == tar:
                target = index
            else:
                pass
        #if target:
        links.append({"source": source, "target": target})
    output["links"] = links
    with open('data/data.json', 'w') as fp:
        json.dump(output, fp)

if __name__=="__main__":
    set_env_vars()
    spotipy_call("Victor Valero")
    write_output()