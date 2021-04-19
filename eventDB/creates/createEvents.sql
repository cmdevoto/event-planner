create table events
(eventID number(3),
 description varchar(100), 
 eventTime date,
 location varchar(50),
 ownerUsername varchar(20),
 associatedGroup number(3), 
 accessStatus varchar(7),
 associatedSchool varchar(30),
 creatorUsername varchar(20),
 CONSTRAINT eventsPK PRIMARY KEY (eventID),
 CONSTRAINT eventsOwnerFK FOREIGN KEY (ownerUsername) references users (username),
 CONSTRAINT eventsCreatorFK FOREIGN KEY (creatorUsername) references users (username),
 CONSTRAINT eventsGroupFK FOREIGN KEY (associatedGroup) references groups (groupID)
);
