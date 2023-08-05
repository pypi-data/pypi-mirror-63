trellotool
==========
An experiment in building a CLI for trello

Development Installation
========================

You should run this in a venv. Do something like this:

```
$ python3 -m venv ~/venv3
$ . ~/venv3/bin/activate
$ mkdir -p ~/src
$ git clone https://github.com/mrda/trellotool.git
$ cd trellotool
$ pip install -U pip
$ pip install -Ur requirements.txt
$ pip install -e .
```

Installing a Release
====================

That's what pypi is for!

```
$ pip install --user trellotool
```

Usage
=====
Trellis has the concept of boards, lists and cards.  Cards as part of lists, and lists are part of boards.  To start with, you need to define which board you want to use by default, and what lists are used for what things.  This is how you do that:
```
$ trellotool board list # this will show you all the boards you have available to access
$ trellotool board set 5d718f75a279e72b4a96baca # this sets a default board
```
Now, let's see what lists are defined on your board, and define which boards are which:
```
$ trellotool list list
Board: Your Board Name
+--------------------------+-------------------+
| id                       | name              |
+--------------------------+-------------------+
| 5d7191360fd4b323358fc535 | Backlog           |
| 5d718975a279e7274a9ebacb | To Do             |
| 5d718975a279e7274a9ebacc | In Progress       |
| 5d7170831e61ac479bef4177 | Blocked           |
| 5d7190f431d7303469954aff | In Review         |
| 5d718fa5a279e7274a9ebacd | Done              |
| 5e6021f2206bff6e61047d01 | Ready to archive? |
+--------------------------+-------------------+
$ trellotool list set todo 5d718975a279e7274a9ebacb
$ trellotool list set backlog 5d7191360fd4b323358fc535
$ trellotool list set in_progress 5d718975a279e7274a9ebacc
```
This completes the setup we need to do.  To see what cards are available on each of your boards, you can do this:
```
$ trellotool card list todo
+--------------------------+--------------------------------------------------------------------------------------+------+--------------+-----------------+-------------------------------+
| id                       | name                                                                                 | due  | due complete | members         | short url                     |
+--------------------------+--------------------------------------------------------------------------------------+------+--------------+-----------------+-------------------------------+
| 5d76d71a0cb04361ce4dc240 | Research random things about giraffes                                                | None | False        | michaeldubya    | https://trello.com/c/dM4BSIKV |
| 5d71b669bb06553eaeceb376 | Eat a whole jar of peanut butter in one day                                          | None | False        | anthonysmith    | https://trello.com/c/hTsXmvHC |
| 5d76eb2a91e7815d38797338 | Sync some tracks for the boys                                                        | None | False        | steadytevor     | https://trello.com/c/0gBfOpDG |
| 5e666c42656a3e4fefdeadb3 | Preliminary pep8 compliance for new code module                                      | None | False        | jeremiahthefrog | https://trello.com/c/w6zbMQ6A |
| 5db6f5d99cf4cd3da85f4ae8 | Get status reports in on time by writing a reminder script                           | None | False        | jeremiahthefrog | https://trello.com/c/7ZrdTfCl |
| 5d726e09da03b65fac9972f1 | Improve unit test coverage on the legacy modul we just included                      | None | False        | jeremiahthefrog | https://trello.com/c/yyzwbF1L |
+--------------------------+--------------------------------------------------------------------------------------+------+--------------+-----------------+-------------------------------+
```
and you can do the same for other boards, by replacing "todo" with either "in_progress" or "backlog".

Next step is to add some cards to a board:
```
$ trellotool card add "Add F30 support to mongrel-punt"
```
And if you're ever uncertain about what commands are available, or what parameters they require, you can just append 'help' on the end of any command or subcommand for assistance.  i.e.
```
$ trellotool help
Available commands for trellotool are: board, card, help, list
board <subcommand>
card <subcommand>
help - Display help information
list <subcommand>
$ trellotool card help
Available commands for card are: add, help, list
add [-e] <card title> [<list>] - Add a new card to your list, defaults to <backlog> if not specified, optionally allowing you to edit the description of the new card
help - Display help information
list - List all cards for the current list
$ trellotool card add
[-e] <card title> [<list>] - Add a new card to your list, defaults to <backlog> if not specified, optionally allowing you to edit the description of the new card
```
