create table eventInvitations
(eventID number(3),
 inviterUsername varchar(20),
 inviteeUsername varchar(20),
 invitationMessage varchar(100),
 CONSTRAINT eventInvitationsPK PRIMARY KEY (eventID, inviterUsername, inviteeUsername),
 CONSTRAINT inviterFK FOREIGN KEY (inviterUsername) references users (username),
 CONSTRAINT inviteeFK FOREIGN KEY (inviteeUsername) references users (username),
 CONSTRAINT eventInvitationsFK FOREIGN KEY (eventID) references events (eventID)
);
