# Copyright (C) 2018-2019 SignalFx, Inc. All rights reserved.
from traceback import format_exc

import opentracing
import requests.sessions
from opentracing.ext import tags
from opentracing.propagation import Format

from biz_monitor.biz_tracing.tracer import inc_level


class SessionTracing(requests.sessions.Session):

    def __init__(self, tracer=None, propagate=True, span_tags=None):
        self._tracer = tracer or opentracing.tracer
        self._propagate = propagate
        self._span_tags = span_tags or {}
        super(SessionTracing, self).__init__()

    def request(self, method, url, *args, **kwargs):
        lower_method = method.lower()
        with self._tracer.start_active_span('requests.{}'.format(lower_method)) as scope:
            span = scope.span
            inc_level(span)
            span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
            span.set_tag(tags.COMPONENT, 'requests')
            span.set_tag(tags.HTTP_METHOD, lower_method)
            span.set_tag(tags.HTTP_URL, url)
            for name, value in self._span_tags.items():
                span.set_tag(name, value)

            if self._propagate:
                headers = kwargs.setdefault('headers', {})
                try:
                    self._tracer.inject(span.context, Format.HTTP_HEADERS, headers)
                except opentracing.UnsupportedFormatException:
                    pass
            try:
                resp = super(SessionTracing, self).request(method, url, *args, **kwargs)
                span.set_tag(tags.HTTP_STATUS_CODE, resp.status_code)
            except Exception:
                span.set_tag(tags.ERROR, True)
                span.set_tag('error.object', format_exc())
                raise

        return resp


def monkeypatch_requests():
    requests.Session = SessionTracing
    requests.sessions.Session = SessionTracing
