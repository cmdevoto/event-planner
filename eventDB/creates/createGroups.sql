create table groups
 (groupID number(3),
 groupName varchar(20),
 groupDesc varchar(30),
 ownerUsername varchar(20),
 CONSTRAINT groupsPK PRIMARY KEY (groupID),
 CONSTRAINT groupUsername FOREIGN KEY (ownerUsername) references users (username)
);

create sequence group_seq start with 1;

create or replace trigger group_tr
before insert on groups
for each row

begin
  select group_seq.NEXTVAL
  into :new.groupID
  from dual;
end;
/
