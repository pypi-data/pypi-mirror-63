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
"""End-to-end tests against a live server."""
import pkgutil
import os

from requests.exceptions import HTTPError
from requests.status_codes import codes
import pytest

from .. import Client


def get_coinc_xml_bytes():
    return pkgutil.get_data(__name__, os.path.join('data/coinc.xml'))


@pytest.fixture
def coinc_xml_bytes():
    return get_coinc_xml_bytes()


def authenticated_client_or_skip():
    """Return an authenticated client, or skip the test."""
    try:
        return Client('https://gracedb-test.ligo.org/api/',
                      fail_if_noauth=True)
    except ValueError:
        pytest.skip('no GraceDB credentials found')


def skip_if_not_authorized(client):
    """Do test upload to see if we have permissions."""
    try:
        event = client.events.create(
            filename='coinc.xml', filecontents=get_coinc_xml_bytes(),
            group='Test', pipeline='gstlal')
        graceid = event['graceid']
        superevent = client.superevents.create(
            preferred_event=graceid,
            t_start=1000000000.12345678,
            t_0=1000000001.12345678,
            t_end=1000000002.12345678)
        superevent_id = superevent['superevent_id']
        client.superevents[superevent_id].expose()
    except HTTPError as e:
        if e.response.status_code == codes.FORBIDDEN:
            pytest.skip('GraceDB credentials not authorized for gracedb-test')
        else:
            raise


@pytest.fixture(scope='module')
def client():
    with authenticated_client_or_skip() as client:
        skip_if_not_authorized(client)
        yield client


@pytest.mark.parametrize('labels_in,labels_out', [
    [{'EM_READY', 'DQV'}, ['EM_READY', 'DQV']],
    [['EM_READY', 'DQV'], ['EM_READY', 'DQV']],
    [('EM_READY', 'DQV'), ['EM_READY', 'DQV']],
    ['EM_READY', ['EM_READY']],
    [['EM_READY'], ['EM_READY']],
    [None, []],
    [[], []]
])
def test_events_create(client, coinc_xml_bytes, labels_in, labels_out):
    result = client.events.create(
        filename='coinc.xml', filecontents=coinc_xml_bytes,
        group='Test', pipeline='gstlal', labels=labels_in)
    assert set(result['labels']) == set(labels_out)


@pytest.fixture
def events_create(client, coinc_xml_bytes):
    return client.events.create(
        filename='coinc.xml', filecontents=coinc_xml_bytes,
        group='Test', pipeline='gstlal')


def test_events_get(client, events_create):
    event_id = events_create['graceid']
    result = client.events[event_id].get()
    assert events_create == {**result, 'warnings': []}


def test_events_update(client, events_create, coinc_xml_bytes):
    event_id = events_create['graceid']
    client.events.update(
        event_id, filename='coinc.xml',
        filecontents=coinc_xml_bytes + b'<!--foobar-->')


def test_events_search(client, events_create):
    event_id = events_create['graceid']
    result = list(client.events.search(query=event_id))
    assert len(result) == 1
    assert events_create == {**result[0], 'warnings': []}


@pytest.fixture
def events_labels_create(client, events_create):
    event_id = events_create['graceid']
    return client.events[event_id].labels.create('SKYMAP_READY')


def test_events_events_labels_create(client, events_create,
                                     events_labels_create):
    event_id = events_create['graceid']
    result = client.events[event_id].labels.get()
    assert result[0]['name'] == 'SKYMAP_READY'


def test_events_labels_delete(client, events_create, events_labels_create):
    event_id = events_create['graceid']
    client.events[event_id].labels.delete('SKYMAP_READY')
    result = client.events[event_id].labels.get()
    assert len(result) == 0


@pytest.mark.parametrize('filename,filecontents', [
    [None, None],
    ['foo.txt', 'bar']
])
@pytest.mark.parametrize('tags_in,tags_out', [
    [['emfollow', 'p_astro'], ['emfollow', 'p_astro']],
    ['emfollow', ['emfollow']],
    [None, []]
])
def test_events_logs_create(client, events_create, filename, filecontents,
                            tags_in, tags_out):
    event_id = events_create['graceid']
    result = client.events[event_id].logs.create(
        comment='plugh', filename=filename, filecontents=filecontents,
        tags=tags_in)
    if filename is None:
        assert result['filename'] == ''
    else:
        assert result['filename'] == filename
    assert set(result['tag_names']) == set(tags_out)


def test_events_logs_get(client, events_create):
    event_id = events_create['graceid']
    result = client.events[event_id].logs.get()
    assert result[0]['filename'] == 'coinc.xml'


def test_events_files_get(client, events_create):
    event_id = events_create['graceid']
    result = client.events[event_id].files.get()
    assert 'coinc.xml' in result


def test_events_files_get_alternate(client, events_create):
    event_id = events_create['graceid']
    result = client.superevents[event_id].files.get()
    assert 'coinc.xml' in result


def test_events_files_file_get(client, events_create):
    event_id = events_create['graceid']
    client.events[event_id].logs.create(
        comment='plugh', filename='foo.txt', filecontents=b'bar')
    with client.events[event_id].files['foo.txt'].get() as f:
        filecontents = f.read()
    assert filecontents == b'bar'


@pytest.fixture
def events_logs_tags_create(client, events_create):
    event_id = events_create['graceid']
    client.events[event_id].logs[1].tags.create('em_bright')


def test_events_logs_tags_create(client, events_create,
                                 events_logs_tags_create):
    event_id = events_create['graceid']
    result = client.events[event_id].logs[1].tags.get()
    assert result[0]['name'] == 'em_bright'


def test_events_logs_tags_delete(client, events_create,
                                 events_logs_tags_create):
    event_id = events_create['graceid']
    client.events[event_id].logs[1].tags.delete('em_bright')
    result = client.events[event_id].logs[1].tags.get()
    assert len(result) == 0


@pytest.fixture
def events_voevents_create(client, events_create):
    event_id = events_create['graceid']
    return client.events[event_id].voevents.create(voevent_type='earlywarning')


def test_events_voevents_create(client, events_create, events_voevents_create):
    event_id = events_create['graceid']
    filename = '{}-1-EarlyWarning.xml'.format(event_id)
    assert events_voevents_create['filename'] == filename


def test_events_voevents_get(client, events_create, events_voevents_create):
    event_id = events_create['graceid']
    result = client.events[event_id].voevents.get()
    assert len(result) == 1
    filename = '{}-1-EarlyWarning.xml'.format(event_id)
    assert result[0]['filename'] == filename


@pytest.fixture
def superevents_create(client, events_create):
    event_id = events_create['graceid']
    return client.superevents.create(
        preferred_event=event_id,
        t_start=1000000000.12345678,
        t_0=1000000001.12345678,
        t_end=1000000002.12345678)


def test_superevents_create(client, events_create, superevents_create):
    event_id = events_create['graceid']
    assert superevents_create['preferred_event'] == event_id
    assert superevents_create['t_start'] == 1000000000.123457
    assert superevents_create['t_0'] == 1000000001.123457
    assert superevents_create['t_end'] == 1000000002.123457


def test_superevents_get(client, superevents_create):
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].get()
    assert superevents_create == result


def test_superevents_search(client, superevents_create):
    superevent_id = superevents_create['superevent_id']
    query = '{} category: Test'.format(superevent_id)
    result = list(client.superevents.search(query=query))
    assert [superevents_create] == result


def test_superevents_update(client, superevents_create):
    superevent_id = superevents_create['superevent_id']
    client.superevents.update(superevent_id, t_start=123, t_0=456, t_end=789)
    result = client.superevents[superevent_id].get()
    assert result['t_start'] == 123
    assert result['t_0'] == 456
    assert result['t_end'] == 789


def test_superevents_update_preferred_event_none(client, superevents_create):
    # Regression test for https://git.ligo.org/emfollow/gracedb-sdk/issues/13
    superevent_id = superevents_create['superevent_id']
    client.superevents.update(superevent_id, preferred_event=None,
                              t_start=123, t_0=456, t_end=789)
    result = client.superevents[superevent_id].get()
    assert result['t_start'] == 123
    assert result['t_0'] == 456
    assert result['t_end'] == 789


def test_superevents_update_preferred_event_same(client, events_create,
                                                 superevents_create):
    # Check that passing current preferred event is OK
    superevent_id = superevents_create['superevent_id']
    event_id = events_create['graceid']
    client.superevents.update(superevent_id, preferred_event=event_id,
                              t_start=123, t_0=456, t_end=789)
    result = client.superevents[superevent_id].get()
    assert result['t_start'] == 123
    assert result['t_0'] == 456
    assert result['t_end'] == 789


@pytest.fixture
def events_create_2(client, coinc_xml_bytes):
    return client.events.create(
        filename='coinc.xml', filecontents=coinc_xml_bytes,
        group='Test', pipeline='gstlal')


@pytest.fixture
def superevents_add(client, superevents_create, events_create_2):
    event_id_2 = events_create_2['graceid']
    superevent_id = superevents_create['superevent_id']
    client.superevents[superevent_id].add(event_id_2)


def test_superevents_add(client, superevents_add, superevents_create,
                         events_create, events_create_2):
    event_id = events_create['graceid']
    event_id_2 = events_create_2['graceid']
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].get()
    assert set(result['gw_events']) == {event_id, event_id_2}
    assert result['preferred_event'] == event_id


@pytest.fixture
def superevents_update_change_preferred_event(client, superevents_create,
                                              events_create_2):
    event_id_2 = events_create_2['graceid']
    superevent_id = superevents_create['superevent_id']
    client.superevents.update(superevent_id, preferred_event=event_id_2)


def test_superevents_update_change_preferred_event(
        client, superevents_add, superevents_create,
        superevents_update_change_preferred_event, events_create,
        events_create_2):
    event_id = events_create['graceid']
    event_id_2 = events_create_2['graceid']
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].get()
    assert set(result['gw_events']) == {event_id, event_id_2}
    assert result['preferred_event'] == event_id_2


def test_superevents_remove(client, superevents_add, superevents_create,
                            events_create, events_create_2):
    event_id = events_create['graceid']
    event_id_2 = events_create_2['graceid']
    superevent_id = superevents_create['superevent_id']
    client.superevents[superevent_id].remove(event_id_2)
    result = client.superevents[superevent_id].get()
    assert set(result['gw_events']) == {event_id}


@pytest.fixture
def superevents_labels_create(client, superevents_create):
    superevent_id = superevents_create['superevent_id']
    return client.superevents[superevent_id].labels.create('SKYMAP_READY')


def test_superevents_superevents_labels_create(client, superevents_create,
                                               superevents_labels_create):
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].labels.get()
    assert result[0]['name'] == 'SKYMAP_READY'


def test_superevents_labels_delete(client, superevents_create,
                                   superevents_labels_create):
    superevent_id = superevents_create['superevent_id']
    client.superevents[superevent_id].labels.delete('SKYMAP_READY')
    result = client.superevents[superevent_id].labels.get()
    assert len(result) == 0


@pytest.mark.parametrize('filename,filecontents', [
    [None, None],
    ['foo.txt', 'bar']
])
@pytest.mark.parametrize('tags_in,tags_out', [
    [['emfollow', 'p_astro'], ['emfollow', 'p_astro']],
    ['emfollow', ['emfollow']],
    [None, []]
])
def test_superevents_logs_create(client, superevents_create, filename,
                                 filecontents, tags_in, tags_out):
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].logs.create(
        comment='plugh', filename=filename, filecontents=filecontents,
        tags=tags_in)
    if filename is None:
        assert result['filename'] == ''
    else:
        assert result['filename'] == filename
    assert set(result['tag_names']) == set(tags_out)


@pytest.fixture
def superevents_logs_create(client, superevents_create):
    superevent_id = superevents_create['superevent_id']
    return client.superevents[superevent_id].logs.create(
        comment='plugh', filename='foo.txt', filecontents='bar')


def test_superevents_logs_get(client, superevents_create,
                              superevents_logs_create):
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].logs.get()
    assert result[-1]['filename'] == 'foo.txt'


def test_superevents_files_get(client, superevents_create,
                               superevents_logs_create):
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].files.get()
    assert 'foo.txt' in result


def test_superevents_files_get_alternate(client, superevents_create,
                                         superevents_logs_create):
    superevent_id = superevents_create['superevent_id']
    result = client.events[superevent_id].files.get()
    assert 'foo.txt' in result


def test_superevents_files_file_get(client, superevents_create,
                                    superevents_logs_create):
    superevent_id = superevents_create['superevent_id']
    with client.superevents[superevent_id].files['foo.txt'].get() as f:
        filecontents = f.read()
    assert filecontents == b'bar'


@pytest.fixture
def superevents_logs_tags_create(client, superevents_create,
                                 superevents_logs_create):
    superevent_id = superevents_create['superevent_id']
    client.superevents[superevent_id].logs[1].tags.create('em_bright')


def test_superevents_logs_tags_create(client, superevents_create,
                                      superevents_logs_tags_create):
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].logs[1].tags.get()
    assert result[0]['name'] == 'em_bright'


def test_superevents_logs_tags_delete(client, superevents_create,
                                      superevents_logs_tags_create):
    superevent_id = superevents_create['superevent_id']
    client.superevents[superevent_id].logs[1].tags.delete('em_bright')
    result = client.superevents[superevent_id].logs[1].tags.get()
    assert len(result) == 0


@pytest.fixture
def superevents_voevents_create(client, superevents_create):
    superevent_id = superevents_create['superevent_id']
    return client.superevents[superevent_id].voevents.create(
        voevent_type='earlywarning')


def test_superevents_voevents_create(client, superevents_create,
                                     superevents_voevents_create):
    superevent_id = superevents_create['superevent_id']
    filename = '{}-1-EarlyWarning.xml'.format(superevent_id)
    assert superevents_voevents_create['filename'] == filename


def test_superevents_voevents_get(client, superevents_create,
                                  superevents_voevents_create):
    superevent_id = superevents_create['superevent_id']
    result = client.superevents[superevent_id].voevents.get()
    filename = '{}-1-EarlyWarning.xml'.format(superevent_id)
    assert len(result) == 1
    assert result[0]['filename'] == filename


def test_superevents_expose(client, superevents_create):
    superevent_id = superevents_create['superevent_id']
    client.superevents[superevent_id].expose()
    assert client.superevents[superevent_id].is_exposed()
    client.superevents[superevent_id].unexpose()
    assert not client.superevents[superevent_id].is_exposed()


@pytest.mark.parametrize('status', ['OK', 'NO'])
def test_superevents_signoff_operator(client, superevents_create, status):
    superevent_id = superevents_create['superevent_id']

    # We generally don't have permission to do operator signoffs.
    with pytest.raises(HTTPError) as exc_info:
        client.superevents[superevent_id].signoff('H1', status, comment='foo')
    assert exc_info.value.response.status_code == 403


@pytest.mark.parametrize('status', ['OK', 'NO'])
def test_superevents_signoff_advocate(client, superevents_create, status):
    superevent_id = superevents_create['superevent_id']
    client.superevents[superevent_id].labels.create('ADVREQ')
    client.superevents[superevent_id].signoff('ADV', status, comment='foo')
    result = client.superevents[superevent_id].labels.get()
    labels = {row['name'] for row in result}
    assert 'ADV' + status in labels
