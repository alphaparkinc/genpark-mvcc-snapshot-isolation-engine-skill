import sys
import json
from client import MVCCEngine

def main():
    engine = MVCCEngine()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "begin":
            view = engine.begin_transaction()
            res = {"tx_view": view}
        elif method == "write":
            ok, msg = engine.write(params.get("tx_view"), params.get("key"), params.get("value"))
            res = {"status": ok, "message": msg}
        elif method == "read":
            val = engine.read(params.get("tx_view"), params.get("key"))
            res = {"value": val}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
