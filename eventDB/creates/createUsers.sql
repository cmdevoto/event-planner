create table users
(username varchar(20),
 firstName varchar(20),
 lastName varchar(20),
 passwordHash varchar(20),
 email varchar(320),
 associatedSchool varchar(50),
 CONSTRAINT usersPK PRIMARY KEY (username)
);
