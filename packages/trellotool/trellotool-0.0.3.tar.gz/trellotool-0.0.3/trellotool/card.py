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

import prettytable

from trellotool import command
from trellotool import config
from trellotool import trellolist
from trellotool import trello_if
from trellotool import utils


class Card:
    """Representation of a Card
    https://developers.trello.com/reference/#card-object
    """

    card_explanation = \
        ("#\n"
         "# This is the description section of your new ticket.  You can use\n"
         "# Markdown here.  For example:\n"
         "#\n"
         "# This is a First Level Header\n"
         "# ============================\n"
         "#\n"
         "# This is a Second Level Header\n"
         "# -----------------------------\n"
         "#\n"
         "# You can **Bold** things, _underline_ things, and add *emphasis*\n"
         "#\n"
         "# This is a list:\n"
         "# - spam\n"
         "# - eggs\n"
         "# - bacon, and\n"
         "# - spam\n"
         "#\n"
         "# Want more [spam](https://www.dailymotion.com/video/x2hwqlw)?\n")

    def __init__(self):
        self.cmd = command.Command('card')
        self.cmd.add('add', self.add,
                     help_text=("[-e] <card title> [<list>] - Add a new card"
                                " to your list, defaults to <backlog> if not"
                                " specified, optionally allowing you to edit"
                                " the description of the new card"))
        self.cmd.add('list', self.list,
                     help_text="- List all cards for the current list")
        self.cmd.add('show', self.show,
                     help_text="<card-id> - Show card fields")
        self.cmd.add('move', self.move, help_text=("<card-id> <list-id>"
                     "- Move card <card-id> to <list-id>"))

    def add(self, args=None):
        if utils.debug:
            print("Invoking card.add with {}".format(args))
        try:

            if args is None or len(args) < 1 or len(args) > 3:
                self.cmd.usage_for_cmd('add')
                return

            # Default params
            launch_editor = False
            tlist = trellolist.TrelloList.default_list_for_addition
            title = None
            description = ""
            found_title = False
            unknown_param = False

            # Time to parse arguments.  Note that the valid options are:
            # [-e] <card title> [<tlist>]
            # i.e. '-e' and '<tlist>' are optional
            for arg in args:
                if arg == '-e':
                    launch_editor = True
                elif arg in trellolist.TrelloList.allowed_default_list:
                    tlist = arg
                else:
                    # Only option left is that this is a title
                    if not found_title:
                        title = arg
                        found_title = True
                    else:
                        print("Unknown parameter")
                        unknown_param = True

            # There are a limited set of arguments allowed, they are:
            # 1) trellotool add title
            # 2) trellotool add -e title
            # 3) trellotool add title tlist
            # 4) trellotool add -e title tlist
            # i.e. title is mandatory
            if title is None or unknown_param:
                self.cmd.usage_for_cmd('add')
                return

            if launch_editor:
                description = \
                    utils.launch_editor_with_explanation(Card.card_explanation)

            if utils.debug:
                print("title is '{}'".format(title))
                print("tlist is '{}'".format(tlist))
                print("description is '{}'".format(description))

            trello_if.add_card(tlist, title, description)

        except Exception as e:
            print("Error: Could not add card ({})".format(e))

    def list(self, args=None):
        if utils.debug:
            print("Invoking card.list with {}".format(args))
        try:

            if args is None:
                print("--- No list specified, defaulting to 'In Progress'")
                curr_list_id = config.get_in_progress_list()[0]
            elif (len(args) != 1 or
                  args[0] not in trellolist.TrelloList.allowed_default_list):

                print("Error: You need to provide a list name, one of {}"
                      .format(", ".join("'{}'".format(a) for a in
                              trellolist.TrelloList.allowed_default_list)))
                return
            elif args[0] == "in_progress":
                curr_list_id = config.get_in_progress_list()[0]
            elif args[0] == "todo":
                curr_list_id = config.get_todo_list()[0]
            elif args[0] == "backlog":
                curr_list_id = config.get_backlog_list()[0]

            if curr_list_id is None:
                print("Error: Could not access list.  Have you set it?")
                return

            table = prettytable.PrettyTable()
            table.field_names = ['id', 'name', 'due', 'due complete',
                                 'members', 'short url']
            for f in table.field_names:
                table.align[f] = 'l'

            cards = trello_if.get_cards(curr_list_id)
            for card in cards:
                m_info = []
                for m in card.member_ids:
                    member_obj = trello_if.get_member_info(m)
                    m_info.append(member_obj.username)
                usernames_str = ", ".join(m for m in m_info)
                table.add_row([card.id, card.name, card.due,
                              card.is_due_complete, usernames_str,
                              card.shortUrl])
            print(table)
        except Exception as e:
            print("Error: Could not list cards ({})".format(e))

    def show(self, args=None):
        if utils.debug:
            print("Invoking card.show with {}".format(args))
        try:
            if args is None or len(args) != 1:
                print("Error: No card specified")
                return

            card = trello_if.get_card(args[0])

            table = prettytable.PrettyTable()
            table.field_names = ['field', 'value']
            for f in table.field_names:
                table.align[f] = 'l'
            table.add_row(["name", card.name])
            table.add_row(["id", args[0]])
            table.add_row(["last activity", card.date_last_activity])
            # table.add_row(["pos", card.pos])
            table.add_row(["short url", card.shortUrl])
            # table.add_row(["url", card.url])
            table.add_row(["description", card.desc])
            table.add_row(["due", card.due])
            table.add_row(["is due complete", card.is_due_complete])

            members = []
            table.add_row(["closed", card.closed])
            for m in card.member_ids:
                member = trello_if.get_member_info(m)
                members.append(member.username)
            table.add_row(["members", ", ".join(m for m in members)])

            # table.add_row(["idLabels", card.idLabels])
            table.add_row(["board", trello_if.get_board(card.idBoard).name])
            table.add_row(["list", trello_if.get_list(card.idList).name])
            # table.add_row(["idShort", card.idShort])
            # table.add_row(["badges", card.badges])
            print(table)

        except Exception as e:
            print("Error: Could not show card ({})".format(e))

    def move(self, args=None):
        if utils.debug:
            print("Invoking card.move with {}".format(args))

        try:
            if args is None or len(args) != 2:
                print("Error: No card or list specified")
                self.cmd.usage_for_cmd('move')
                return

            try:
                card = trello_if.get_card(args[0])
            except Exception as e:
                print("Error: Could not move card. Invalid card id.")
                self.cmd.usage_for_cmd('move')
                return

            try:
                # Allow aliasing on common lists
                tlist = args[1]
                if tlist in trellolist.TrelloList.allowed_default_list:
                    tlist = config.get_list_id_by_name(tlist)
                tlist = trello_if.get_list(tlist)
            except Exception as e:
                print("Error: Could not move card. Invalid list id.({})"
                      .format(e))
                self.cmd.usage_for_cmd('move')
                return

            if utils.debug:
                print("Moving card '{}' to '{}'".format(card.name, tlist.name))

            card.change_list(tlist.id)

        except Exception as e:
            print("Error: Could not move card ({})".format(e))
