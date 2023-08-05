# -*- coding: utf-8 -*-

# Copyright (c) 2016 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of Wirecloud.

# Wirecloud is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Wirecloud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Wirecloud.  If not, see <http://www.gnu.org/licenses/>.

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

from wirecloud.live.utils import build_group_name, WIRECLOUD_BROADCAST_GROUP


@channel_session_user_from_http
def ws_connect(message):
    user_group = build_group_name("live-%s" % message.user.username)
    Group(user_group).add(message.reply_channel)
    Group(WIRECLOUD_BROADCAST_GROUP).add(message.reply_channel)
    message.reply_channel.send({"accept": True})


@channel_session_user
def ws_disconnect(message):
    user_group = build_group_name("live-%s" % message.user.username)
    Group(user_group).discard(message.reply_channel)
    Group(WIRECLOUD_BROADCAST_GROUP).discard(message.reply_channel)
