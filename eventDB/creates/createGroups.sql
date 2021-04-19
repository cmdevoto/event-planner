create table groups
 (groupID number(3),
 groupName varchar(20),
 groupDesc varchar(30),
 ownerUsername varchar(20),
 CONSTRAINT groupsPK PRIMARY KEY (groupID),
 CONSTRAINT groupUsername FOREIGN KEY (ownerUsername) references users (username)
);
