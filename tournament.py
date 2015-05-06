#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2

# Connect to the PostgreSQL database.  Returns a database connection.


def connect():
    return psycopg2.connect("dbname='tournament'")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    cur.execute("DELETE FROM MATCHES")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    cur.execute("DELETE FROM players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    cur.execute("SELECT count(*) as TotalPlayers from players")
    TotalPlayers = cur.fetchone()
    return TotalPlayers[0]
    conn.close()

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    cur.execute("SELECT count(*) as TotalPlayers from players")
    row = cur.fetchone()
    TotalPlayers = row[0]
    if TotalPlayers == 0:
        # restart the playerserial count
        cur.execute("ALTER SEQUENCE players_playerID_seq RESTART WITH 1")
    # INSERT a new player
    cur.execute("INSERT INTO players (playerfullname) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    First entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Standings")
    return cur.fetchall()
    conn.commit()
    conn.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    cur.execute("INSERT INTO matches (winnerID, loserID) \
    VALUES (%s,%s)", (winner, loser))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Standings")
    # store current standing based on TotalWins
    Current_Standing = cur.fetchall()
    totalPlayers = len(Current_Standing)
    paired_list = [0]  # declare list/array variable to store list of pairs
    for x in range(0, totalPlayers, 2):
        Paired_Players = Current_Standing[x][0], Current_Standing[x][1], \
                        Current_Standing[x+1][0], Current_Standing[x+1][1]
        paired_list.append(Paired_Players)
    paired_list.remove(0)
    return paired_list
    conn.close()
