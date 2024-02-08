create table notes(
    id integer primary key,
    user_id integer,
    topic varchar(255),
    description text,
    date varchar(255),
    file varchar(255),
    foreign key(user_id) references users(user_id) on delete cascade
);


create table to_do_list(
    id integer primary key,
    user_id integer,
    topic varchar(255),
    description text,
    date varchar(255),
    foreign key (user_id) references users (user_id) on delete cascade
);

create table users(
    user_id primary key,
    first_enter text,
    name varchar(100)
)

