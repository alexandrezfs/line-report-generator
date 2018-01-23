from service.line_server_factory import LineServerFactory

if __name__ == "__main__":
    LineServerFactory() \
        .get_instance() \
        .run()
