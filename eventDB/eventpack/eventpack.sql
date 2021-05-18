create or replace package eventpack 
as
  function checkValidAccess(username users.username%type, eventId events.eventID%type)
    return varchar2;
end eventpack;
/