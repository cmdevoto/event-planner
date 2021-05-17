load data infile 'csv/polls.csv'
insert into table polls
fields terminated by "," optionally enclosed by '"'
(eventID, ownerUsername, title, description)
