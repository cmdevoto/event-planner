drop table eventGroups;
drop table groupMembership;
drop table eventPostings;
drop table eventInvitations;
drop table events;
drop table groups;
drop table users; 

@creates/createUsers.sql
@creates/createGroups.sql
@creates/createEvents.sql
@creates/createEventInvitations.sql
@creates/createEventPostings.sql
@creates/createGroupMembership.sql
@creates/createEventGroups.sql

Exit;
