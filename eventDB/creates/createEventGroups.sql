create table eventGroups
(eventID number(3),
 groupID number(3),
 groupName varchar(20),
 CONSTRAINT eventGroupsPK PRIMARY KEY (eventID, groupID),
 CONSTRAINT eventGroupsEventFK FOREIGN KEY (eventID) references events (eventID),
 CONSTRAINT eventGroupsGroupFK FOREIGN KEY (groupID) references groups (groupID)
);
