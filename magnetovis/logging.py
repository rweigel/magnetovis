import traceback
import time
from datetime import timedelta

import logging
logging.basicConfig(
    format='%(delta)s.%(msecs)03d:%(filename)s:%(funcName)s(): %(message)s',
    level=logging.INFO,
    datefmt='%S')

class CustomStreamHandler(logging.StreamHandler):
    # The primary motivation for this custom stream handler
    # is that logging.info() text appears in the Paraview output messages
    # tab in red, which makes it seem that the message is an error.
    # In addition, default background is dark brown and so it is difficult
    # to read the messages when the font is red.
    # When print() is used, the color appears as green.

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
                    #print(frame_summary)
                    indentation_level += 1
        #if not hasattr(self, 'last_indentation_level'):
        #    self.last_indentation_level = indentation_level
        #print(indentation_level)
        indent = indentation_level - 1 # - self.last_indentation_level
        #self.last_indentation_level = indentation_level

        msg = self.format(record).split(":")
        msg = msg[0] + ": " + 2*indent*" " + ":".join(msg[1:])
        print(msg, flush=True)

ch = CustomStreamHandler()
ch.setFormatter(logging.root.handlers[0].formatter)
logger = logging.getLogger(__name__)
logger.addHandler(ch)
logger.propagate = False # Only call CustomStreamHandler()
logger.info("Called.")
