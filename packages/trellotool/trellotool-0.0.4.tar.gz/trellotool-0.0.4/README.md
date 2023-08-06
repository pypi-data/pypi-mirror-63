trellotool
==========
A CLI for [trello](https://trello.com/)

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
Trellotool has the concept of boards, lists and cards.  Cards as part of lists, and lists are part of boards.  To start with, you need to define which board you want to use by default, and what lists are used for what things.  This is how you do that:
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
+--------------------------+------------------------------------------------------------------+------+--------------+-----------------+-------------------------------+
| id                       | name                                                             | due  | due complete | members         | short url                     |
+--------------------------+------------------------------------------------------------------+------+--------------+-----------------+-------------------------------+
| 5d76d71a0cb04361ce4dc240 | Research random things about giraffes                            | None | False        | michaeldubya    | https://trello.com/c/dM4BSIKV |
| 5d71b669bb06553eaeceb376 | Eat a whole jar of peanut butter in one day                      | None | False        | anthonysmith    | https://trello.com/c/hTsXmvHC |
| 5d76eb2a91e7815d38797338 | Sync some tracks for the boys                                    | None | False        | steadytevor     | https://trello.com/c/0gBfOpDG |
| 5e666c42656a3e4fefdeadb3 | Preliminary pep8 compliance for new code module                  | None | False        | jeremiahthefrog | https://trello.com/c/w6zbMQ6A |
| 5db6f5d99cf4cd3da85f4ae8 | Get status reports in on time by writing a reminder script       | None | False        | jeremiahthefrog | https://trello.com/c/7ZrdTfCl |
| 5d726e09da03b65fac9972f1 | Improve unit test coverage on the legacy module we just included | None | False        | jeremiahthefrog | https://trello.com/c/yyzwbF1L |
+--------------------------+------------------------------------------------------------------+------+--------------+-----------------+-------------------------------+
```
and you can do the same for other boards, by replacing "todo" with either "in_progress" or "backlog".

Next step is to add some cards to a board:
```
$ trellotool card add "Add F30 support to mongrel-punt"
```

And of course, it's always important to be able to view cards:
```
$ trellotool card show 5d726e09da03b65fac9972f1
+-----------------+-----------------------------------------------------------------------+
| field           | value                                                                 |
+-----------------+-----------------------------------------------------------------------+
| name            | Improve unit test coverage on the legacy module we just included      |
| id              | 5e30901187796e2335676f06                                              |
| last activity   | 2020-03-09 19:54:15.045000+00:00                                      |
| shortUrl        | https://trello.com/c/yyzwbF1                                          |
| desc            | Improve the test coverage by examing cover and look for low-hanging   |
|                 | fruit, and to improve the functionality that is covered by our tests. |
| due             | None                                                                  |
| is due complete | False                                                                 |
| closed          | False                                                                 |
| members         | jeremiahthefrog                                                       |
+-----------------+-----------------------------------------------------------------------+
```
You can also move cards between lists, with support for list aliases:
```
trellotool card move 5e30901187796e2335676f06 todo
trellotool card move 5e30901187796e2335676f06 5d718fa5a279e7274a9ebacd # move to the Done list
```
Getting Help
------------
If you're ever uncertain about what commands are available, or what parameters they require, you can just append 'help' on the end of any command or subcommand for assistance.  i.e.
```
$ trellotool help
Available commands for trellotool are: board, card, help, list
board <subcommand>
card <subcommand>
help - Display help information
list <subcommand>
$ trellotool card help
Available commands for card are: add, help, list, move, show
add [-e] <card title> [<list-alias> | <list-id>] - Add a new card to an optionally specified <list-alias> or <list-id>, if not specified, defaults to the <backlog> list. If provided, -e will invoke $EDITOR, allowing you to provide the new card's description
help - Display help information
list - List all cards for the current list
move <card-id> (<list-alias> | list-id>) - Move card <card-id> to the list specified by either the <list-alias> or <list-id>
show <card-id> - Show card fields
```
