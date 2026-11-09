"""Launch Indra's viewer on all interfaces inside the Docker container."""

import indra_ocr.viewer as viewer
from http.server import ThreadingHTTPServer as BaseThreadingHTTPServer


class PublicThreadingHTTPServer(BaseThreadingHTTPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        host, port = server_address
        super().__init__(("0.0.0.0", port), RequestHandlerClass, bind_and_activate)


viewer.ThreadingHTTPServer = PublicThreadingHTTPServer
viewer.main()
