create table if not exists MUZ_GENRES (
	ID serial primary key,
	NAME varchar(100) not null
);

create table if not exists muz_artists (
	ID serial primary key,
	NAME varchar(100) not null,
	birth_date date,
	alias varchar(100)
);

create table if not exists MUZ_ART_GENRE (
	ID serial primary key,
	art_id integer not null references muz_artists(id),
	genre_id integer not null references MUZ_GENRES(id)
);





create table if not exists muz_albums (
	ID serial primary key,
	NAME varchar(100) not null,
	rate integer check(rate > 0),
	year integer check (year > 1900 and year < 2100)
);

create table if not exists MUZ_ART_ALBUM (
	ID serial primary key,
	art_id integer not null references muz_artists(id),
	album_id integer not null references muz_albums(id)
);

create table if not exists muz_tracks (
	ID serial primary key,
	NAME varchar(100) not null,
	dur integer check(dur > 0),
	album_id integer references muz_albums(id)
);

create table if not exists muz_collections (
	ID serial primary key,
	NAME varchar(100) not null,
	year integer check(year > 1900 and year < 2100)
);

create table if not exists MUZ_COLL_TRACKS (
	ID serial primary key,
	track_id integer not null references muz_tracks(id),
	coll_id  integer not null references muz_collections(id)
);