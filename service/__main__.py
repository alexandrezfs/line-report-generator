'''
Service entry point.
Get a server from the factory, and run it.
'''

from service.config import LINE_REPORT_GENERATOR_PORT
from service.line_server_factory import LineServerFactory

if __name__ == "__main__":
    LineServerFactory() \
        .get_instance() \
        .run(port=int(LINE_REPORT_GENERATOR_PORT))
