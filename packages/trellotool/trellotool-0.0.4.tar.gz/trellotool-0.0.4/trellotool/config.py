#!/usr/bin/env python
#
# config.py - data storage for trellotool
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

import appdirs
import datetime
import errno
import json
import os
import pathlib
import sys

from trellotool import utils


DEFAULT_BOARD = 'default_board'

BACKLOG_LIST = 'backlog'
TODO_LIST = 'todo'
IN_PROGRESS_LIST = 'in_progress'
TRELLO_API_KEY = 'TRELLO_API_KEY'
TRELLO_API_SECRET = 'TRELLO_API_SECRET'
LAST_MODIFIED = 'last-modified'

_user = os.environ.get('USER')
_name = os.path.basename(sys.argv[0])
_config_dir = appdirs.user_config_dir(_name, _user)
_save_file = "{}-config.json".format(_name)
_filename = os.path.join(_config_dir, _save_file)
_data = {}


def _init():
    # Initialise the location for stored data
    try:
        pathlib.Path(_config_dir).mkdir(parents=True)
    except OSError as e:
        # Allow directory already exists to be squashed.
        # Otherwise allow it to bubble up
        if e.errno != errno.EEXIST:
            raise


def _load():
    global _data
    try:
        _init()
        with open(_filename, "r") as f:
            _data = json.load(f)
        if utils.debug:
            print(_data)
    except IOError:
        pass


def _save():
    global _data
    try:
        _init()
        _data[LAST_MODIFIED] = \
            datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        with open(_filename, "w") as f:
            json.dump(_data, f, indent=4)
    except IOError:
        print("Can't save {}".format(_filename))


def get_credentials():
    """Return back the credentials to access Trello"""
    global _data
    _load()

    # First, check to see if we can get the credentials from
    # environment variables
    api_key = os.environ.get("TRELLO_API_KEY")
    api_secret = os.environ.get("TRELLO_API_SECRET")

    # If that didn't work, we try from the config file
    if api_key is None:
        try:
            api_key = _data[TRELLO_API_KEY]
        except KeyError:
            # Allow for an in place upgrade
            _data[TRELLO_API_KEY] = ""
            _save()

    if api_secret is None:
        try:
            api_secret = _data[TRELLO_API_SECRET]
        except KeyError:
            # Allow for an in place upgrade
            _data[TRELLO_API_SECRET] = ""
            _save()

    cmd = os.path.basename(sys.argv[0])
    err = False

    if api_key is None or api_key == "":
        print("{}: You need to have TRELLO_API_KEY set in either an"
              .format(cmd))
        print("environment variable, or in the config file.")
        print("You can obtain this from visiting https://trello.com/app-key"
              " and copying the key")
        print("into your shell, like this, 'export TRELLO_API_KEY=sjkfhksdhf"
              "jksdhfkjsdhfk'")
        print()
        err = True

    if api_secret is None or api_secret == "":
        print("{}: You need to have TRELLO_API_SECRET set in either an"
              .format(cmd))
        print("environment variable, or in the config file.")
        print("You can obtain this from visiting https://trello.com/app-key"
              " and generating a Token")
        print("and copy that into your shell, like this,"
              "'export TRELLO_API_SECRET=dkfjg9045jgl'")
        print()
        err = True

    if err:
        print("Exiting...")
        sys.exit(1)

    return api_key, api_secret


def set(field, data):
    _load()
    _data[field] = data
    _save()


def get(field):
    _load()
    return _data[field]


def set_default_board(id, name):
    d = {'id': id, 'name': name}
    set(DEFAULT_BOARD, d)


def get_default_board():
    _load()
    try:
        id = _data[DEFAULT_BOARD]['id']
        name = _data[DEFAULT_BOARD]['name']
        return id, name
    except KeyError:
        return None, None


def get_backlog_list():
    return get_list_meta_by_name(BACKLOG_LIST)


def set_backlog_list(id, name):
    d = {'id': id, 'name': name}
    set(BACKLOG_LIST, d)


def get_todo_list():
    return get_list_meta_by_name(TODO_LIST)


def set_todo_list(id, name):
    d = {'id': id, 'name': name}
    set(TODO_LIST, d)


def get_in_progress_list():
    return get_list_meta_by_name(IN_PROGRESS_LIST)


def set_in_progress_list(id, name):
    d = {'id': id, 'name': name}
    set(IN_PROGRESS_LIST, d)


def get_list_id_by_name(name):
    _load()
    for elem in _data:
        try:
            if elem == name:
                return _data[elem]['id']
        except Exception as e:
            # Some elements won't have the required fields, so we can just skip
            pass
    return None


def get_list_meta_by_name(name):
    _load()
    for elem in _data:
        try:
            if elem == name:
                return _data[elem]['id'], _data[elem]['name']
        except Exception as e:
            # Some elements won't have the required fields, so we can just skip
            pass
    return None, None
