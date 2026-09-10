from client import MVCCEngine

def main():
    print("=== Testing MVCC Snapshot Isolation Engine ===")
    mvcc = MVCCEngine()
    t1 = mvcc.begin_transaction()
    mvcc.write(t1, "balance:alice", 1000)

    t2 = mvcc.begin_transaction()
    val_t2 = mvcc.read(t2, "balance:alice")
    print("t2 sees balance:alice =>", val_t2)
    assert val_t2 == 1000

    t3 = mvcc.begin_transaction()
    mvcc.write(t3, "balance:alice", 1500)
    print("t3 reads balance:alice =>", mvcc.read(t3, "balance:alice"))
    print("t2 still reads balance:alice =>", mvcc.read(t2, "balance:alice"))

    assert mvcc.read(t3, "balance:alice") == 1500
    assert mvcc.read(t2, "balance:alice") == 1000
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
