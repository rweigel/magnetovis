import traceback
import time
from datetime import timedelta

import logging
logger = logging.getLogger("magnetovis")

class CustomStreamHandler(logging.StreamHandler):

    # The primary motivation for this custom stream handler
    # is that logging.info() text appears in the Paraview output messages
    # tab in red, which makes it seem that the message is an error.
    # In addition, the default console background can be set to dark
    # brown in which case it is difficult to read the messages when
    # the font is red.

    def format(self, record):

        # Based on https://stackoverflow.com/a/58943125
        import datetime
        duration = datetime.datetime.utcfromtimestamp(record.relativeCreated / 1000)
        record.delta = duration.strftime("%S")
        return super().format(record)

    def emit(self, record):

        indentation_level = 0
        frame_summaries = traceback.extract_stack()
        for frame_summary in frame_summaries:
            if 'logging' not in frame_summary.filename:
                if 'magnetovis' in frame_summary.filename:
                    indentation_level += 1
        indent = indentation_level - 1
        msg = self.format(record).split(":")
        msg = msg[0] + ": " + 2*indent*" " + ":".join(msg[1:])

        if record.levelno == 40:
            # Error
            print("! " + msg.replace("\n","\n! "), flush=True)
        else:
            print(msg, flush=True)


ch = CustomStreamHandler()
formatter = logging.Formatter('%(delta)s.%(msecs)03d:magnetovis:%(filename)s:%(funcName)s(): %(message)s', '%S')
ch.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(ch)
logger.propagate = False # Only call CustomStreamHandler()
