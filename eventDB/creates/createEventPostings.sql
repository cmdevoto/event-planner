create table eventPostings
 (postID number(3),
 eventID number(3),
 ownerUsername varchar(20),
 postContent varchar(100),
 CONSTRAINT eventPostingsPK PRIMARY KEY (postID),
 CONSTRAINT eventPostingsEventFK FOREIGN KEY (eventID) references events (eventID),
 CONSTRAINT eventPostingsUsernameFK FOREIGN KEY (ownerUsername) references users (username)
);
