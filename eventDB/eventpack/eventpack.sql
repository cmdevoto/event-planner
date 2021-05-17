create or replace package eventpack 
as
  function checkValidAccess(username user.username%type, eventId events.eventID%type)

end eventpack;
/