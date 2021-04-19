load data infile 'csv/eventPostings.csv'
insert into table eventPostings
fields terminated by "," optionally enclosed by '"'
(postID, eventID, ownerUsername, postContent)
