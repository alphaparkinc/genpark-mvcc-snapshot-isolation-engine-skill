import sys
import json
from client import MVCCEngine

engine = MVCCEngine()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "mvcc_operation",
                        "description": "Perform write, snapshot read, or vacuum on MVCC engine",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["write", "read", "vacuum"]},
                                "key": {"type": "string"},
                                "value": {"type": ["string", "number", "object", "null"]},
                                "ts": {"type": "number"}
                            },
                            "required": ["action", "ts"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "mvcc_operation":
            action = args["action"]
            ts = args["ts"]
            if action == "write":
                engine.write(args["key"], args["value"], ts)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"status": "WRITTEN", "key": args["key"], "write_ts": ts})}]}}
            elif action == "read":
                val = engine.read(args["key"], ts)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"key": args["key"], "read_ts": ts, "value": val})}]}}
            elif action == "vacuum":
                count = engine.vacuum(ts)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"vacuumed_versions": count, "oldest_active_ts": ts})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
