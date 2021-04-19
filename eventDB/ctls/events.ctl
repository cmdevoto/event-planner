load data infile 'csv/events.csv'
insert into table events
fields terminated by "," optionally enclosed by '"'
(eventID, description, eventTime date "YYYY/MM/DD hh24:mi:ss", location, ownerUsername, associatedGroup, accessStatus, associatedSchool, creatorUsername)
