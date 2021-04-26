load data infile 'csv/groups.csv'
insert into table groups
fields terminated by "," optionally enclosed by '"'
(groupName, groupDesc, ownerUsername)
