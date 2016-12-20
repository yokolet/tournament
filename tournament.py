#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def execute_query(query, args=None, result=False):
    """Utility function to execute a query.

    This function takes a query, optional args, and a result flag.
    The query can be delete or insert sql statement. The args are assumed to
    be given as a tuple. When the result is required, set result flag to True.
    """
    cursor = connect().cursor()
    if args:
        cursor.execute(query, args)
    else:
        cursor.execute(query)
    values = None
    if result:
        values = cursor.fetchall()
    cursor.close()
    return values


def deleteMatches():
    """Remove all the match records from the database."""
    query = "delete from matches; commit;"
    execute_query(query)


def deletePlayers():
    """Remove all the player records from the database."""
    query = "delete from players; commit;"
    execute_query(query)


def countPlayers():
    """Returns the number of players currently registered."""
    query = "select count(*) as num from players;"
    values = execute_query(query, result=True)
    count = values[0][0]
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    query = "insert into players(name) values (%s); commit;"
    execute_query(query, (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = """select p.id, p.name,
      (select count(*) from matches where matches.winner = p.id) as wins,
      (select count(*) from matches where matches.loser = p.id
                                          or matches.winner = p.id) as matches
    from players as p
    order by wins desc;"""
    values = execute_query(query, result=True)
    return values


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = "insert into matches (winner, loser) values (%s, %s); commit;"
    execute_query(query, args=(winner, loser))


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
    standings = playerStandings()
    pairs = []
    idx = 0
    l = len(standings)
    while idx < l:
        player1 = standings[idx]
        idx += 1
        if idx < l:
            player2 = standings[idx]
            #  in each standing, index 0 is an id, and index 1 is a name
            pairs.append((player1[0], player1[1], player2[0], player2[1]))
            idx += 1
    return pairs
