class MVCCEngine:
    """
    Multi-Version Concurrency Control (MVCC) engine with Snapshot Isolation
    and optimistic conflict detection.
    """
    def __init__(self):
        self.global_tx_counter = 1
        self.rows = {}

    def begin_transaction(self):
        tx_id = self.global_tx_counter
        self.global_tx_counter += 1
        read_view = {"tx_id": tx_id, "snapshot_time": tx_id}
        return read_view

    def write(self, tx_view, key, value):
        tx_id = tx_view["tx_id"]
        if key not in self.rows:
            self.rows[key] = []
        for v in self.rows[key]:
            if v["created_by"] > tx_view["snapshot_time"] or (v["deleted_by"] and v["deleted_by"] > tx_view["snapshot_time"]):
                return False, "WRITE_CONFLICT_DETECTED"
            if v["deleted_by"] is None:
                v["deleted_by"] = tx_id
        self.rows[key].append({"created_by": tx_id, "deleted_by": None, "val": value})
        return True, "OK"

    def read(self, tx_view, key):
        tx_id = tx_view["tx_id"]
        if key not in self.rows:
            return None
        for v in reversed(self.rows[key]):
            created_ok = (v["created_by"] <= tx_view["snapshot_time"] or v["created_by"] == tx_id)
            if v["deleted_by"] == tx_id:
                continue
            if created_ok and (v["deleted_by"] is None or v["deleted_by"] > tx_view["snapshot_time"]):
                return v["val"]
        return None
