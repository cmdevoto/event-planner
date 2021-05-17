create or replace package eventpack 
as
  function checkValidAccess(username user.username%type, eventId events.eventID%type)
    return VARCHAR2
  is
    cursor inviteCheck (un user.username%type, eid events.eventID%type)
    is
      select status
      frrom eventInvitations eInv
      where eInv.eventID = eid and eInv.inviteeUsername = un;
    cursor eventData (eid events.eventID%type)
    is
      select ownerUsername, creatorUsername
      from events e
      where e.ownerUsername = eid or e.creatorUsername = eid;
    eventOwner events.ownerUsername%type;
    eventCreator events.creatorUsername%type;
    eventInvStatus eventInvitations.status%type;
    begin
      open(eventData);
      loop
        fetch eventData into eventOwner, eventCreator;
        exit when eventData%notfound;
        return 'true';
      end loop;
      close eventData;

      open(inviteCheck);
      loop
          fetch inviteCheck into eventInvStatus;
          exit when inviteCheck%notfound;
          return 'true';
      end loop;
      close inviteCheck;
      return 'false';
    end;

end eventpack;
/