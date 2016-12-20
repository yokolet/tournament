# Swiss system tournament

This repository has an application to perform Swiss system tournament.
The application consists of three files:

- Application: `tournamnet.py`
- SQL table definition: `tournament.sql
- Test: `tournament_test.py`

This application is written to run on PostgreSQL 9.3.15.

## Usage

To run the code, create a database and tables first.
Then, run the tests.

1. create a database, `tournament`

    ```
    $ psql
    psql (9.3.15)
    Type "help" for help.

    vagrant=> create database tournament;
    CREATE DATABASE
    ```

2. create tables

   ```
   forum=> \c tournament
   You are now connected to database "tournament" as user "vagrant".

   tournament=> \i tournament.sql
   CREATE TABLE
   CREATE TABLE
   ```

3. run tests

   ```bash
   $ python tournament_test.py

   1. countPlayers() returns 0 after initial deletePlayers() execution.
   2. countPlayers() returns 1 after one player is registered.
   3. countPlayers() returns 2 after two players are registered.
   4. countPlayers() returns zero after registered players are deleted.
   5. Player records successfully deleted.
   6. Newly registered players appear in the standings with no matches.
   7. After a match, players have updated standings.
   8. After match deletion, player standings are properly reset.
   9. Matches are properly deleted.
   10. After one match, players with one win are properly paired.
   Success!  All tests pass!
   ```
