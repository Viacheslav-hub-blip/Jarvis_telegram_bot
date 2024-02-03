create table notes(
    id integer primary key,
    topic varchar(255),
    description text,
    date varchar(255),
    file blob
)


create table to_do_list(
    id integer primary key,
    topic varchar(255),
    description text,
    date varchar(255)
)

