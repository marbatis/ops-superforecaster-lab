
def test_health(client) -> None:
    assert client.get("/api/health").status_code == 200


def test_submit_and_resolve_flow(client) -> None:
    qid = "q_cpu_spike"
    submit = client.post(
        f"/api/questions/{qid}/forecast",
        json={"participant": "marcelo", "probability": 0.6, "source_type": "human"},
    )
    assert submit.status_code == 200

    resolve = client.post(f"/api/questions/{qid}/resolve", json={"event_occurred": False})
    assert resolve.status_code == 200

    board = client.get("/api/leaderboard")
    assert board.status_code == 200
    assert "leaderboard" in board.json()
