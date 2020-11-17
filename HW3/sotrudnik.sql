create table if not exists sotrudnik (
	id serial primary key,
	name varchar(100) not null,
	department varchar(100),
	parent_id integer references sotrudnik(id)
);