"""Multi-Version Concurrency Control (MVCC) Snapshot Isolation Engine.
100% Python Standard Library.
"""

import collections

class MVCCEngine:
    """Multi-Version Concurrency Control (MVCC) with snapshot isolation."""
    class Version:
        def __init__(self, val, created_ts, expired_ts=float("inf")):
            self.val = val
            self.created_ts = created_ts
            self.expired_ts = expired_ts

    def __init__(self):
        self.data = collections.defaultdict(list)

    def write(self, key, val, write_ts):
        versions = self.data[key]
        for v in versions:
            if v.expired_ts == float("inf"):
                v.expired_ts = write_ts
        versions.append(self.Version(val, created_ts=write_ts))

    def read(self, key, read_ts):
        for v in self.data[key]:
            if v.created_ts <= read_ts < v.expired_ts:
                return v.val
        return None

    def vacuum(self, oldest_active_ts):
        deleted_count = 0
        for key in list(self.data.keys()):
            new_versions = []
            for v in self.data[key]:
                if v.expired_ts <= oldest_active_ts:
                    deleted_count += 1
                else:
                    new_versions.append(v)
            self.data[key] = new_versions
        return deleted_count
