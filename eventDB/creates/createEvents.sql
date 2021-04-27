create table events
(eventID number(3),
 description varchar(100), 
 eventTime date,
 location varchar(50),
 ownerUsername varchar(20),
 accessStatus varchar(7),
 associatedSchool varchar(50),
 creatorUsername varchar(20),
 CONSTRAINT eventsPK PRIMARY KEY (eventID),
 CONSTRAINT eventsOwnerFK FOREIGN KEY (ownerUsername) references users (username),
 CONSTRAINT eventsCreatorFK FOREIGN KEY (creatorUsername) references users (username)
);

create sequence event_seq start with 1;

create or replace trigger event_tr
before insert on events
for each row

begin
  select event_seq.NEXTVAL
  into :new.eventID
  from dual;
end;
/
