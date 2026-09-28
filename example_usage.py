from client import MVCCEngine

mvcc = MVCCEngine()
mvcc.write("account_balance", 1000.0, write_ts=10)
mvcc.write("account_balance", 1250.0, write_ts=20)
mvcc.write("account_balance", 800.0, write_ts=30)

print("Balance at ts=15:", mvcc.read("account_balance", read_ts=15))
print("Balance at ts=25:", mvcc.read("account_balance", read_ts=25))
print("Balance at ts=35:", mvcc.read("account_balance", read_ts=35))

cleaned = mvcc.vacuum(oldest_active_ts=20)
print(f"Vacuumed {cleaned} stale versions prior to ts=20.")
