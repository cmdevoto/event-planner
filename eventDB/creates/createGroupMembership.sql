create table groupMembership
(username varchar(20),
 groupID number(3),
 status varchar(10),
 invitationMessage varchar(30),
 CONSTRAINT groupMembershipPK PRIMARY KEY (username, groupID),
 CONSTRAINT groupMembershipUsernameFK FOREIGN KEY (username) references users (username),
 CONSTRAINT groupIDFK FOREIGN KEY (groupID) references groups (groupID)
);
