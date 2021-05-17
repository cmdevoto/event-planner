load data infile 'csv/pollRequest.csv'
insert into table pollRequest
fields terminated by "," optionally enclosed by '"'
(pollID, requestedUsername, status)
