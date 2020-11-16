create table if not exists MUZ_GENRES (
	ID serial primary key,
	NAME varchar(100) not null
);

create table if not exists muz_artists (
	ID serial primary key,
	NAME varchar(100) not null,
	birth_date date,
	alias varchar(100),
	genre_id integer references muz_genres(id)
);

create table if not exists muz_albums (
	ID serial primary key,
	NAME varchar(100) not null,
	rate integer check(rate > 0),
	year integer check (year > 1900 and year < 2100),
	artist_id integer references muz_artists(id)
);

create table if not exists muz_tracks (
	ID serial primary key,
	NAME varchar(100) not null,
	dur integer check(dur > 0),
	album_id integer references muz_albums(id)
);