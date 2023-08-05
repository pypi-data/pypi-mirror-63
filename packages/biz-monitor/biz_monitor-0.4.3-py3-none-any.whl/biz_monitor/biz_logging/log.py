import logging
import time

import opentracing
from flask import _request_ctx_stack as stack


def init_logging(service_name, idc_name, set_name, instance_id, level=logging.INFO):
    class Formatter(logging.Formatter):
        def format(self, record):
            msg = super().format(record)
            trace_id = getattr(opentracing.tracer.active_span, "trace_id", "") if stack.top else ""
            return f"[{idc_name},{set_name},{service_name},{instance_id},{trace_id},{int(time.time() * 1000)}]:{record.levelname}:{msg}"

    log = logging.getLogger()
    # Jaeger client has already initialized root logger, purge the StreamHandler
    log.handlers = [hdlr for hdlr in log.handlers if not isinstance(hdlr, logging.StreamHandler)]

    log.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(Formatter())
    log.addHandler(console_handler)
    return log
