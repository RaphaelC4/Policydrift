# test_flow.py - call sequence for GenLayer Studio (type params WITHOUT quote
# marks). Use a policy page you have read yourself.

def run(contract):
    contract.register_policy(policy_id="demo", url="https://www.spotify.com/legal/end-user-agreement/").transact()

    # First snapshot is number 1. Expect a JSON list of clause ids.
    print(contract.file_snapshot(policy_id="demo", expected_index=1).transact())
    print(contract.get_snapshot(policy_id="demo", index=1).call())

    # Filing 1 again must be rejected: "expected_index must be 2".
    # Later, when the page changes (or to test no-change):
    contract.file_snapshot(policy_id="demo", expected_index=2).transact()
    print(contract.get_latest_drift(policy_id="demo").call())
    # "unchanged": true if the page has not changed; otherwise added/removed.

    # Must be rejected: duplicate policy_id, bad URL, unknown policy,
    # more than 6 snapshots, get_drift on a missing snapshot.

if __name__ == "__main__":
    print(__doc__)
