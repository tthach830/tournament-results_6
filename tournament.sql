-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop database if exists tournament;
create database tournament;

\c tournament

drop table if exists players CASCADE;
create table players (
  PlayerFullName varchar,
  PlayerID serial primary key
);

drop table if exists matches CASCADE;
create table matches (
  WinnerID int references players(PlayerID),
  LoserID int references players(PlayerID),
  ID serial primary key
);

INSERT INTO players VALUES ('Dan Thach');
INSERT INTO players VALUES ('Ben Thach');
INSERT INTO players VALUES ('Leo Thach');
INSERT INTO players VALUES ('Lily Thach');
SELECT * FROM players;

--- Insert matches ---------------

INSERT INTO matches VALUES (1,2);
INSERT INTO matches VALUES (3,4);
INSERT INTO matches VALUES (1,3);
INSERT INTO matches VALUES (2,4);
SELECT * FROM matches;

--------Counnt Total Matches for each player
CREATE VIEW TotalMatches AS
    select players.PlayerFullName, players.playerID, count(matches.WinnerID)
    as TotalMatches
    from players
    left join matches
    on matches.winnerID = players.PlayerID or matches.LoserID = players.PlayerID
    group by players.PlayerID;

--------Count Total Wins for each player
CREATE VIEW TotalWins AS
    select Players.PlayerID, Players.PlayerFullName, count(matches.WinnerID)
    as TotalWins
    from Players
    left join matches
    on matches.WinnerID = players.PlayerID
    group by players.PlayerFullName, Players.PlayerID
    order by TotalWins desc;

CREATE VIEW Standings AS
    select TotalWins.playerID,TotalWins.PlayerFullName,TotalWins.TotalWins,
    TotalMatches.TotalMatches
    from TotalWins
    left join TotalMatches
    on TotalWins.playerID = TotalMatches.PlayerID
    order by TotalWins desc;
