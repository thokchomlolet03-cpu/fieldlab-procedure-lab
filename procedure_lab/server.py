"""Loopback-only demo server. Run with python3 -m procedure_lab.server."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .engine import analyze

PRIORITY = "Rush orders go first."
FINISH = "Once packing an order has started, finish that order before switching."
ORIGINAL = f"{PRIORITY} {FINISH}"
REPAIRS = {
    "label_printed": "Packing starts when the label is printed.",
    "first_item_placed": "Packing starts when the first item is placed in the carton.",
}
INDEX = Path(__file__).with_name("index.html")


def example_proposal(text):
    text = text.strip()
    if text == ORIGINAL:
        readings = [{"starts_at": boundary, "quote": FINISH} for boundary in REPAIRS]
    else:
        readings = [{"starts_at": boundary, "quote": sentence}
                    for boundary, sentence in REPAIRS.items()
                    if text == f"{ORIGINAL} {sentence}"]
    if not readings:
        return {"status": "outside_scope", "readings": [],
                "reason": "Curated mode supports the original example and its two repairs. Select Local Meta model to test other wording."}
    return {"status": "interpreted", "readings": readings,
            "rush_priority_quote": PRIORITY, "finish_started_quote": FINISH}


def procedure_test(text, mode):
    if not isinstance(text, str) or not 1 <= len(text.strip()) <= 4000:
        raise ValueError("Enter a procedure of 1 to 4,000 characters.")
    if mode == "example":
        proposal = example_proposal(text)
        source = "curated_example"
    elif mode == "model":
        from . import model
        proposal = model.propose(text)
        source = "local_meta_model"
    else:
        raise ValueError("Choose example or model mode.")
    result = analyze(text, proposal)
    readings = result["readings"]
    def view(case):
        if case is None:
            return None
        return {"arrival": case["position"], "events": case["events"],
                "actions": [case["actions"][r["starts_at"]] for r in readings]}
    return {
        "status": result["status"], "reason": result.get("reason"), "source": source,
        "interpretations": [dict(boundary=r["starts_at"], quote=r["quote"]) for r in readings],
        "cases": [view(case) for case in result["cases"]], "witness": view(result["witness"]),
        "post_finish_control": view(result["post_finish_control"]),
        "searched_traces": result["searched_traces"], "preconditions": result["preconditions"],
    }


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, payload, content_type="application/json"):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def local_request(self):
        port = self.server.server_port
        allowed = {f"127.0.0.1:{port}", f"localhost:{port}"}
        return (self.headers.get("Host") in allowed and
                self.headers.get("Origin") in {None, *("http://" + host for host in allowed)})

    def do_GET(self):
        if not self.local_request():
            return self.reply(403, {"error": "Local origin required."})
        if urlsplit(self.path).path == "/":
            return self.reply(200, INDEX.read_bytes(), "text/html")
        return self.reply(404, {"error": "Unknown route."})

    def do_POST(self):
        if not self.local_request():
            return self.reply(403, {"error": "Local origin required."})
        if self.path != "/api/analyze":
            return self.reply(404, {"error": "Unknown route."})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 32000 or self.headers.get_content_type() != "application/json":
                raise ValueError("Expected a small JSON body.")
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise ValueError("Expected a JSON object.")
            response = procedure_test(payload.get("text"), payload.get("mode"))
        except (ValueError, UnicodeError) as exc:
            return self.reply(400, {"error": str(exc)})
        except RuntimeError as exc:
            return self.reply(503, {"error": str(exc)})
        return self.reply(200, response)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    a = p.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", a.port), Handler) as server:
        print(f"FieldLab is available at http://127.0.0.1:{server.server_port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
