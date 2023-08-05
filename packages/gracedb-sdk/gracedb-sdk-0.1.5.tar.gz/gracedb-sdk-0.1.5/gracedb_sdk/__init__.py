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
from requests_gracedb import Session

from .api import API

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ('Client',)


class Client(API):
    """GraceDB client session.

    Parameters
    ----------
    url : str
        GraceDB Client URL.
    cert : str, tuple
        Client-side X.509 certificate. May be either a single filename
        if the certificate and private key are concatenated together, or
        a tuple of the filenames for the certificate and private key.
    username : str
        Username for basic auth.
    password : str
        Password for basic auth.
    force_noauth : bool, default=False
        If true, then do not use any authentication at all.
    fail_if_noauth : bool, default=False
        If true, then raise an exception if authentication credentials are
        not provided.
    cert_reload : bool, default=False
        If true, then automatically reload the client certificate before it
        expires.
    cert_cert_reload_timeout : int, default=300
        Reload the certificate this many seconds before it expires.

    Notes
    -----
    When a new Client instance is created, the following sources of
    authentication are tried, in order:

    1.  If the :obj:`force_noauth` keyword argument is true, then perform no
        authentication at all.

    2.  If the :obj:`cert` keyword argument is provided, then use X.509 client
        certificate authentication.

    3.  If the :obj:`username` and :obj:`password` keyword arguments are
        provided, then use basic auth.

    4.  Look for a default X.509 client certificate in:

        a.  the environment variables :envvar:`X509_USER_CERT` and
            :envvar:`X509_USER_KEY`
        b.  the environment variable :envvar:`X509_USER_PROXY`
        c.  the file :file:`/tmp/x509up_u{UID}`, where :samp:`{UID}` is your
            numeric user ID
        d.  the files :file:`~/.globus/usercert.pem` and
            :file:`~/.globus/userkey.pem`

    5.  Read the netrc file [1]_ located at :file:`~/.netrc`, or at the path stored
        in the environment variable :envvar:`NETRC`, and look for a username
        and password matching the hostname in the URL.

    6.  If the :obj:`fail_if_noauth` keyword argument is true, and no
        authentication source was found, then raise a :class:`ValueError`.

    The following methods are supported for events:

    * :samp:`client.events.get()`
    * :samp:`client.events.search(query={query}, sort={sort})`
    * :samp:`client.events.create(filename={filename}, filecontents={filecontents}, group={group}, pipeline={pipeline}, search={search}, labels={labels}, offline={offline})`
    * :samp:`client.events.update({event_id}, filename={filename}, filecontents={filecontents})`
    * :samp:`client.events[{event_id}].get()`
    * :samp:`client.events[{event_id}].files.get()`
    * :samp:`client.events[{event_id}].files[{filename}].get()`
    * :samp:`client.events[{event_id}].labels.get()`
    * :samp:`client.events[{event_id}].labels.create({label})`
    * :samp:`client.events[{event_id}].labels.delete({label})`
    * :samp:`client.events[{event_id}].logs.get()`
    * :samp:`client.events[{event_id}].logs.create(comment={comment}, filename={filename}, filecontents={filecontents}, tags={tags})`
    * :samp:`client.events[{event_id}].logs[{N}].tags.create({tag})`
    * :samp:`client.events[{event_id}].logs[{N}].tags.delete({tag})`
    * :samp:`client.events[{event_id}].voevents.get()`
    * :samp:`client.events[{event_id}].voevents.create(voevent_type={}, internal={internal}, open_alert={open_alert}, hardware_inj={hardware_inj}, skymap_type={skymap_type}, skymap_filename={skymap_filename}, ProbHasNS={ProbHasNS}, ProbHasRemnant={ProbHasRemnant}, BNS={BNS}, NSBH={NSBH}, BBH={BBH}, Terrestrial={Terrestrial}, MassGap={MassGap}, coinc_comment={coinc_comment})`

    Analogous methods are supported for superevents:

    * :samp:`client.superevents.get()`
    * :samp:`client.superevents.search(query={query}, sort={sort})`
    * :samp:`client.superevents.create(t_start={t_start}, t_0={t_0}, t_end={t_end}, preferred_event={preferred_event}, events={events}, labels={labels})`
    * :samp:`client.superevents.update({superevent_id}, t_start={t_start}, t_0={t_0}, t_end={t_end}, preferred_event={preferred_event})`
    * :samp:`client.superevents[{superevent_id}].add({event_id})`
    * :samp:`client.superevents[{superevent_id}].remove({event_id})`
    * :samp:`client.superevents[{superevent_id}].is_exposed()`
    * :samp:`client.superevents[{superevent_id}].expose()`
    * :samp:`client.superevents[{superevent_id}].unexpose()`
    * :samp:`client.superevents[{superevent_id}].signoff({'ADV'|'H1'|'L1'|'V1'}, {'OK'|'NO'}, {comment})`
    * :samp:`client.superevents[{superevent_id}].get()`
    * :samp:`client.superevents[{superevent_id}].files.get()`
    * :samp:`client.superevents[{superevent_id}].files[{filename}].get()`
    * :samp:`client.superevents[{superevent_id}].labels.get()`
    * :samp:`client.superevents[{superevent_id}].labels.create({label})`
    * :samp:`client.superevents[{superevent_id}].labels.delete({label})`
    * :samp:`client.superevents[{superevent_id}].logs.get()`
    * :samp:`client.superevents[{superevent_id}].logs.create(comment={comment}, filename={filename}, filecontents={filecontents}, tags={tags})`
    * :samp:`client.superevents[{superevent_id}].logs[{N}].tags.create({tag})`
    * :samp:`client.superevents[{superevent_id}].logs[{N}].tags.delete({tag})`
    * :samp:`client.superevents[{superevent_id}].voevents.get()`
    * :samp:`client.superevents[{superevent_id}].voevents.create(voevent_type={}, internal={internal}, open_alert={open_alert}, hardware_inj={hardware_inj}, skymap_type={skymap_type}, skymap_filename={skymap_filename}, ProbHasNS={ProbHasNS}, ProbHasRemnant={ProbHasRemnant}, BNS={BNS}, NSBH={NSBH}, BBH={BBH}, Terrestrial={Terrestrial}, MassGap={MassGap}, coinc_comment={coinc_comment})`

    References
    ----------
    .. [1] The .netrc file.
           https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html

    """  # noqa: E501

    def __init__(self, url='https://gracedb.ligo.org/api/', *args, **kwargs):
        super().__init__(url, Session(url=url, *args, **kwargs))

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
