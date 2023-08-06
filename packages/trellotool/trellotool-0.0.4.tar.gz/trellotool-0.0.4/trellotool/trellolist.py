#!/usr/bin/env python
#
# card.py - handle Trello cards
#
# Copyright (C) 2020 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html

import re

import prettytable

from trellotool import command
from trellotool import config
from trellotool import trello_if
from trellotool import utils


class TrelloList:
    """Representation of a List"""

    allowed_default_list = ["in_progress", "todo", "backlog"]
    default_list_for_addition = "backlog"

    def __init__(self):
        self.cmd = command.Command('list')
        self.cmd.add('set', self.set,
                     help_text=" <list> - Set a default list")
        self.cmd.add('list', self.list, help_text="- List available lists")
        self.cmd.add('get', self.get,
                     help_text="[<list name>] - List the default lists")

    def default(self):
        error = False
        if utils.debug:
            print("Invoking list default func")
        try:
            table = prettytable.PrettyTable()
            table.field_names = ['id', 'name']
            for f in table.field_names:
                table.align[f] = 'l'

            for tlist in TrelloList.allowed_default_list:
                if tlist == 'in_progress':
                    list_meta = config.get_in_progress_list()
                elif tlist == 'todo':
                    list_meta = config.get_todo_list()
                elif tlist == 'backlog':
                    list_meta = config.get_backlog_list()
                else:
                    print("Error: Unknown default list category")
                    return

                if list_meta is None or list_meta[0] is None:
                    print("Error: No such default list '{}' defined"
                          .format(tlist))
                    error = True
                else:
                    table.add_row([list_meta[0], list_meta[1]])
            if not error:
                print(table)

        except Exception as e:
            print(("Error: Problem listing defaults lists."
                   "Have you set them? ({})".format(e)))

    def set(self, args):
        if utils.debug:
            print("Invoking list.set with {}".format(args))
        if len(args) != 2:
            print("Error: 'set' takes two parameters, the list name or id")
            return
        if args[0] not in TrelloList.allowed_default_list:
            print("Error: list needs be be on of {}".format(", ".join("'{}'"
                  .format(a) for a in TrelloList.allowed_default_list)))
        try:
            list_category = args[0]
            search_list = args[1]
            found_list = None

            board_meta = config.get_default_board()
            board_obj = trello_if.get_board(board_meta[0])

            for tlist in board_obj.all_lists():
                if search_list in [tlist.id, tlist.name]:
                    found_list = tlist

            if found_list is None:
                print("Error: Could not match '{}' against your list of lists"
                      .format(search_list))
                return

            if list_category == 'in_progress':
                config.set_in_progress_list(found_list.id, found_list.name)
            elif list_category == 'todo':
                config.set_todo_list(found_list.id, found_list.name)
            elif list_category == 'backlog':
                config.set_backlog_list(found_list.id, found_list.name)
            else:
                print("Error: Unknown default list category")

        except Exception as e:
            print("Error: Could not set default list ({})".format(e))

    def get(self, args):
        if utils.debug:
            print("Invoking list.set with {}".format(args))
        if len(args) != 1:
            print(("Error: 'get' takes one parameter, the list name,"
                   "list alias or id"))
            return

        try:
            board_meta = config.get_default_board()
            board_obj = trello_if.get_board(board_meta[0])

            thing = args[0]

            tlist = TrelloList.find_list(args[0], board_obj)
            if tlist is None:
                print("Could not find unique list '{}'".format(args[0]))
            else:
                print("'{}' '{}'".format(tlist.id, tlist.name))

        except Exception as e:
            print("Error: Could not get list ({})".format(e))

    def list(self, args=None):
        if utils.debug:
            print("Invoking list.list with {}".format(args))
        try:
            board_meta = config.get_default_board()
            if board_meta is None or board_meta[0] is None:
                print("Error: No default board set")
                return
            board_obj = trello_if.get_board(board_meta[0])

            table = prettytable.PrettyTable()
            table.field_names = ['id', 'name']
            for f in table.field_names:
                table.align[f] = 'l'

            for tlist in trello_if.get_lists(board_obj):
                if not tlist.closed:
                    table.add_row([tlist.id, tlist.name])
            print("Board: {}".format(board_meta[1]))
            print(table)
        except Exception as e:
            print("Error: Could not list all lists for board ({})".format(e))

    def find_list(thing, board_obj):
        """Find a list by pattern matching on name or id or alias"""
        try:
            tlist_id = None
            if thing in TrelloList.allowed_default_list:
                tlist_id = config.get_list_id_by_name(thing)

            if tlist_id is None:
                # i.e. it's not an alias

                all_tlists_for_board = trello_if.get_lists(board_obj)

                thing_pattern = re.compile(".*{}.*".format(thing),
                                           re.IGNORECASE)

                candidates = []
                for tlist in trello_if.get_lists(board_obj):
                    if thing_pattern.match(tlist.name):
                        if utils.debug:
                            print("{} matches".format(tlist.name))
                        candidates.append(tlist.id)

                if len(candidates) == 1:
                    tlist_id = candidates[0]
                elif len(candidates) > 1:
                    if utils.debug:
                        print("*** Multiple matches for {}".format(thing))
                    return None

            if tlist_id is None:
                # i.e. Must be an id by itself
                tlist_id = thing

            return trello_if.get_list(tlist_id)

        except Exception as e:
            if utils.debug:
                print("*** Could not find list from {} ({})".format(thing, e))
            return None
