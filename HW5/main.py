from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import random


class PostgressAPI():
    """docstring for PostgressAPI"""

    # for randomize collection
    UPPER_COLL = 10

    def __init__(self, conn_string):
        self._conn_string = conn_string
        if type(conn_string) is str:
            print(f"Init connect from string: {conn_string}")
            self._engine = create_engine(self._conn_string)
        elif type(conn_string) is dict:
            print("Init connect from dict:")
            print(conn_string)
            self._engine = create_engine(URL(**conn_string))
        else:
            print("Wrong connection string!")
        self._conn = self._engine.connect()
        self._fk_tables = ["muz_art_genre",
                           "muz_art_album",
                           "muz_coll_tracks"]
        self._main_tables = ["muz_genres",
                             "muz_artists",
                             "muz_collections",
                             "muz_tracks",
                             "muz_albums"]
        self._id = 0
        self.init_params()

    def run(self):
        self.trunc_muz_db()
        print("Begin insert")
        self.fill_db()

    def fill_db(self):
        self.fill_collections()
        self.fill_genres()
        self.fill_artists()

    def fill_artists(self):
        year_min, year_max = 2017, 2021
        for artist in self._muz:
            print(f"Insert data for {artist['name']}")
            artist_id = self.get_id()
            stmt = "insert into muz_artists values" \
                   f"({artist_id}, '{artist['name']}', '{artist['bd']}', '{artist['alias']}')"
            self._conn.execute(stmt)
            # insert artist genres
            for genre in artist["genres"]:
                genre_id = self.get_id()
                stmt = "insert into muz_art_genre values" \
                       f"({genre_id}, {artist_id}, {self._genre_cache[genre]})"
                self._conn.execute(stmt)
            # insert albums
            for album in artist["albums"]:
                album_id = self.get_id()
                rate = random.randint(1, 20)
                year = random.randint(year_min, year_max)
                stmt = "insert into muz_albums values" \
                       f"({album_id}, '{album['name']}', {rate}, {year})"
                self._conn.execute(stmt)
                # add relations
                stmt = "insert into muz_art_album values" \
                       f"({self.get_id()}, {artist_id}, {album_id})"
                self._conn.execute(stmt)
                # insert tracks
                for track in album["tracks"]:
                    track_id = self.get_id()
                    dur = random.randint(60, 400)
                    stmt = "insert into muz_tracks values" \
                           f"({track_id}, '{track}', {dur}, {album_id})"
                    self._conn.execute(stmt)
                    # Add random collections
                    # Collection id -  from 1 to len(coll) + 1
                    coll_id = random.randint(1, self.UPPER_COLL)
                    if coll_id <= len(self._collections):
                        # Add track to collection
                        stmt = "insert into muz_coll_tracks values" \
                               f"({self.get_id()}, {track_id}, {coll_id})"
                        self._conn.execute(stmt)

    def fill_collections(self):
        year_min, year_max = 2017, 2021
        print(f"Insert collections. Years from {year_min} to {year_max}")
        for item in self._collections:
            id = self.get_id()
            year = random.randint(year_min, year_max)
            self._conn.execute("insert into muz_collections values" \
                               f"({id}, '{item}', {year})")

    def fill_genres(self):
        print("Insert genres")
        genre_cache = {}
        for item in self._genres:
            id = self.get_id()
            self._conn.execute("insert into muz_genres values" \
                               f"({id}, '{item}')")
            genre_cache[item] = id
        self._genre_cache = genre_cache
        print(genre_cache)

    def trunc_muz_db(self):
        for data in [self._fk_tables, self._main_tables]:
            for table in data:
                print("Truncate table:", table)
                self._conn.execute(f"truncate {table} CASCADE")

    def get_id(self):
        self._id += 1
        return self._id

    def init_params(self):
        muz = []
        collections = [
            "Gold Collection",
            "Bronze Collection",
            "Platinum Collection",
            "Almaz collection",
            "Wooden collection",
            "Shity collection",
            "Top collection",
            "Random tracks collections"]
        sinatra = {
            "name": "Frank Sinatra",
            "bd": "1915-12-12",
            "alias": "Franky",
            "genres": ["swing", "jaz"],
            "albums": [
                {
                    "name": "Strangers in the night",
                    "tracks": [
                        "Strangers in the Night",
                        "Summer Wind",
                        "Call Me"
                    ]
                },
                {
                    "name": "Song for swinging lovers",
                    "tracks": [
                        "you make me feel so young",
                        "old devil moon",
                        "love is here to stay"
                    ]
                }]
        }
        muz.append(sinatra)
        roling_stones = {
            "name": "Roling Stones",
            "bd": "1943-7-26",
            "alias": "Mick Jagger",
            "genres": ["rock"],
            "albums": [
                {
                    "name": "exile on mains st.",
                    "tracks": [
                        "Rocks off",
                        "Rip this joint",
                        "Casino boogie",
                        "My"
                    ]
                }]
        }
        muz.append(roling_stones)
        pilot = {
            "name": "Pilot",
            "bd": "1972-8-2",
            "alias": "Chert",
            "genres": ["grunge", "rock"],
            "albums": [
                {
                    "name": "nashe nebo",
                    "tracks": [
                        "nebo",
                        "karelia",
                        "48",
                        "Мой"
                    ]
                }]
        }
        muz.append(pilot)
        bb = {
            "name": "beastie boys",
            "bd": "1965-11-20",
            "alias": "Mike D",
            "genres": ["rock", "funk"],
            "albums": [
                {
                    "name": "communication",
                    "tracks": [
                        "sabotage",
                        "tough guy",
                        "do it"
                    ]
                }]
        }
        muz.append(bb)
        moby = {
            "name": "Moby",
            "bd": "1965-9-11",
            "alias": "moby",
            "genres": ["electro", "techno"],
            "albums": [
                {
                    "name": "ambient",
                    "tracks": [
                        "heaven",
                        "sound",
                        "dog",
                        "80",
                        "myopia"
                    ]
                }]
        }
        muz.append(moby)

        self._muz = muz
        self._collections = collections
        genres = set()
        for data in self._muz:
            genres.update(data["genres"])
        self._genres = genres


def main():
    print("Init db connection")
    db = {
        "drivername": "postgres",
        "host": "postgre",
        "port": "5432",
        "username": "postgres",
        "password": "postgres",
        "database": "netology"
    }
    pgAPI = PostgressAPI(db)
    pgAPI.run()


if __name__ == '__main__':
    main()
