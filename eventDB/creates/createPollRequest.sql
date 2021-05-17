create table pollRequest
(pollID number(3),
 requestedUsername varchar(20),
 status varchar(10),
 CONSTRAINT pollRequestPK PRIMARY KEY (requestedUsername, pollID),
 CONSTRAINT pollRequestUsernameFK FOREIGN KEY (requestedUsername) references users (username),
 CONSTRAINT pollIDFK FOREIGN KEY (pollID) references polls (pollID)
);
