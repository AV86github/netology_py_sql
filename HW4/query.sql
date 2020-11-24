--название и год выхода альбомов, вышедших в 2018 году;
select name, year from public.muz_albums a where a.year = 2018


--название и продолжительность самого длительного трека;
select name, dur from public.muz_tracks where dur = (
    select max(dur) from public.muz_tracks
)

--название треков, продолжительность которых не менее 3,5 минуты;
select name from public.muz_tracks where dur >= 3.5 * 60

--названия сборников, вышедших в период с 2018 по 2020 год включительно;
select * from muz_collections where year between 2018 and 2020

--исполнители, чье имя состоит из 1 слова;
select * from muz_artists where  name not like '% %'

--название треков, которые содержат слово "мой"/"my".
select name from muz_tracks
where upper(name) like '%MY%' or upper(name) like '%МОЙ%' 
