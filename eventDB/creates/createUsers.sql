create table users
(username varchar(20),
 firstName varchar(20),
 lastName varchar(20),
 passwordHash varchar(100),
 email varchar(320),
 CONSTRAINT usersPK PRIMARY KEY (username)
);
