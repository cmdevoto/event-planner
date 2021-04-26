load data infile 'csv/users.csv'
insert into table users
fields terminated by "," optionally enclosed by '"'
(username, firstName, lastName, passwordHash, email, associatedSchool)
