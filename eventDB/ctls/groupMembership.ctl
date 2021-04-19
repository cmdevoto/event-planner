load data infile 'csv/groupMembership.csv'
insert into table groupMembership
fields terminated by "," optionally enclosed by '"'
(username, groupID, status, invitationMessage)
