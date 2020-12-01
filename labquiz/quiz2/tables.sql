-- CMPUT 291 Fall 2020 Lab Quiz 2
-- create and populate your database using this file

drop table if exists driver;
drop table if exists car;
drop table if exists drives;

create table driver(
    name    char(10),
    gender  char(1),
    age     integer,
    PRIMARY KEY (name)
);

create table car(
    carID   integer,
    brand       char(10),
    type        char(10),
    color   char(20),
    PRIMARY KEY (carID)
);


create table drives(
    drivername     char(10),
    carID   integer,
    PRIMARY KEY (drivername, carID),
    FOREIGN KEY (drivername) REFERENCES driver(name),
    FOREIGN KEY (carID) REFERENCES car(carID)
);

insert into driver values ('Saeed', 'm', 25);
insert into driver values ('Mike', 'm', 27);
insert into driver values ('Jessy', 'f', 42);
insert into driver values ('Paris', 'f', 31);


insert into car values (1, 'BMW', 'COUPE', 'Black');
insert into car values (2, 'Mazda', 'SEDAN', 'Black');
insert into car values (3, 'Mazda', 'SEDAN', 'Red');
insert into car values (4, 'Ford', 'SEDAN', 'Red');
insert into car values (5, 'Ford', 'SEDAN', 'White');
insert into car values (6, 'BMW', 'COUPE', 'Red');


insert into drives values ('Saeed', 1);
insert into drives values ('Saeed', 6);
insert into drives values ('Mike', 6);
insert into drives values ('Paris', 4);
insert into drives values ('Jessy', 2);