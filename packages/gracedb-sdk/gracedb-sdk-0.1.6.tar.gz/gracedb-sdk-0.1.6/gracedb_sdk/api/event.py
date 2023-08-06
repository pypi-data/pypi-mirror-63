#
# Copyright (C) 2019-2020  Leo P. Singer <leo.singer@ligo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from os.path import join

from .base import Deletable, Mutable, Resource
from .files import Files
from .voevents import EventVOEvents, SupereventVOEvents
from .logs import EventLogs, SupereventLogs
from .labels import EventLabels, SupereventLabels


# FIXME: events have a 'log/' resource whereas superevents have 'logs/'.
# Combine BaseEvent, Event, and Superevent into a single Event class
# once this inconsistency has been fixed.
class BaseEvent(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = Files(self)
        self.logs = self.logs_class(self)
        self.labels = self.labels_class(self)
        self.voevents = self.voevent_class(self)


class Event(BaseEvent):

    labels_class = EventLabels
    logs_class = EventLogs
    voevent_class = EventVOEvents


SIGNOFF_INSTRUMENTS = ['H1', 'L1', 'V1']


class Superevent(BaseEvent):

    labels_class = SupereventLabels
    logs_class = SupereventLogs
    voevent_class = SupereventVOEvents

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._events = SupereventEventList(self)
        # FIXME: GraceDB requires a random / for these URLs!
        # This is inconsistent between events and superevents.
        self.url += '/'

    def add(self, event_id):
        self._events.create(data={'event': event_id})

    def remove(self, event_id):
        self._events.delete(event_id)

    def _modify_permissions(self, action):
        url = join(self.url, 'permissions/modify/')
        self.session.post(url, data={'action': action})

    def is_exposed(self):
        url = join(self.url, 'permissions/')
        result = self.session.get(url).json()
        for row in result['permissions']:
            if row['group'] == 'public_users' \
                    and row['permission'] == 'view_superevent':
                return True
        return False

    def expose(self):
        self._modify_permissions('expose')

    def unexpose(self):
        self._modify_permissions('hide')

    def signoff(self, signoff_type, status, comment=''):
        url = join(self.url, 'signoffs/')
        data = {'status': status, 'comment': comment}
        if signoff_type in SIGNOFF_INSTRUMENTS:
            data['signoff_type'] = 'OP'
            data['instrument'] = signoff_type
        else:
            data['signoff_type'] = signoff_type
            data['instrument'] = ''
        self.session.post(url, data=data)


class SupereventEventList(Deletable, Mutable, Resource):

    path = 'events/'
