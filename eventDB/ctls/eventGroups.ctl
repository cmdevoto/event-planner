load data infile 'csv/eventGroups.csv'
insert into table eventGroups
fields terminated by "," optionally enclosed by '"'
(eventID, groupID, groupName)
