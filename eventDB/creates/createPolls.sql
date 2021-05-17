create table polls
 (pollID number(3),
  eventID number(3),
 ownerUsername varchar(20),
  title varchar (20),
  description varchar (40),
 CONSTRAINT pollsPK PRIMARY KEY (pollID),
 CONSTRAINT pollsEventID FOREIGN KEY (eventID) references events (eventID),
 CONSTRAINT pollsOwnerUsername FOREIGN KEY (ownerUsername) references users (username)
);

create sequence poll_seq start with 1;

create or replace trigger poll_tr
before insert on polls
for each row

begin
  select poll_seq.NEXTVAL
  into :new.pollID
  from dual;
end;
/
