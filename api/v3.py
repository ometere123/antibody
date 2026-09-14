import json
from http.server import BaseHTTPRequestHandler
from vercel_fixture import respond


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            body = json.dumps(respond("/v3", payload.get("input", ""))).encode("utf-8")
            status = 200
        except Exception as exc:
            body = json.dumps({"error": str(exc)}).encode("utf-8")
            status = 400
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return
