--количество исполнителей в каждом жанре;
select b.name ganr, count(1) from muz_art_genre g 
left join muz_genres b on g.genre_id = b.id
group by b.name

--количество треков, вошедших в альбомы 2019-2020 годов;
select count(1) from muz_tracks a
left join muz_albums b on a.album_id = b.id
where b.year in (2019,2020)

--средняя продолжительность треков по каждому альбому;
select b.name, round(avg(dur)::numeric, 2) from muz_tracks a
left join muz_albums b on b.id = a.album_id
group by b.name

--все исполнители, которые не выпустили альбомы в 2020 году;
select * from muz_artists a where not exists (
    select * from muz_art_album b
    left join muz_albums c on c.id = b.album_id
    where c.year = 2020 and b.art_id = a.id
)

--названия сборников, в которых присутствует конкретный исполнитель (выберите сами);

select a.name from muz_collections a where exists (
    select * from muz_coll_tracks b
    left join muz_tracks c on b.track_id = c.id
    left join muz_art_album d on d.album_id = c.album_id
    left join muz_artists e on e.id = d.art_id
    where
    a.id = b.coll_id and
        e.name = 'Frank Sinatra'
)

--название альбомов, в которых присутствуют исполнители более 1 жанра;
select name from (
select distinct a.name, d.genre_id from muz_albums a 
left join muz_art_album b on a.id = b.album_id
left join muz_artists c on c.id = b.art_id
left join muz_art_genre d on d.art_id = c.id
    ) sq1
    group by sq1.name
    having count(1) > 1

--наименование треков, которые не входят в сборники;
select name from muz_tracks a
left join muz_coll_tracks b on a.id = b.track_id
where b.id is null

--исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
select a.name from muz_artists a
left join muz_art_album b on a.id = b.art_id
left join muz_tracks c on c.album_id = b.album_id
where c.dur = (
select min(dur) from muz_tracks
)

--название альбомов, содержащих наименьшее количество треков.
with sq1 as (
select a.name, count(1) cnt from muz_albums a
left join muz_tracks b on a.id = b.album_id
group by a.name
order by cnt
    )
    select name from sq1
    where sq1.cnt = (select min(cnt) from sq1)
