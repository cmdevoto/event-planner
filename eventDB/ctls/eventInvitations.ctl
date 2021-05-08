load data infile 'csv/eventInvitations.csv'
insert into table eventInvitations
fields terminated by "," optionally enclosed by '"'
(eventID, inviterUsername, inviteeUsername, invitationMessage, status)
