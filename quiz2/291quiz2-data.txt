-- Let's drop the tables in case they exist
drop table if exists loan;
drop table if exists deposit;
drop table if exists customer;
drop table if exists branch;

PRAGMA foreign_keys = ON;

create table branch (
  bname 	text,
  address 	text,
  city 		text,
  assets	integer,
  primary key (bname)
);
create table customer (
  cname		text,
  street	text,
  city		text,
  primary key (cname)
);
create table deposit (
  accno		integer,
  cname		text,
  bname		text,
  balance	real,
  primary key (accno),
  foreign key (cname) references customer,
  foreign key (bname) references branch
);
create table loan (
  accno		integer,
  cname		text,
  bname		text,
  amount	real,
  primary key (accno),
  foreign key (cname) references customer,
  foreign key (bname) references branch
);

insert into customer values ('John','Jasper Ave','Edmonton');
insert into customer values ('Davood','114 St','Edmonton');
insert into customer values ('Mary','87 Ave','Calgary');

insert into branch values ('CIBC college plaza','112 St','Edmonton',1000000);
insert into branch values ('BMO UofA','87 Ave','Edmonton',1200000);
insert into branch values ('BMO UofC','87 Ave','Calgary',1000000);

insert into deposit values (100,'Davood','CIBC college plaza',1000);
insert into deposit values (200,'John','CIBC college plaza',1400);
insert into deposit values (300,'Mary','BMO UofA',1100);

insert into loan values (110,'Davood','CIBC college plaza',10000);
insert into loan values (120,'Davood','BMO UofA',20000);
insert into loan values (130,'Mary','BMO UofA',10000);
