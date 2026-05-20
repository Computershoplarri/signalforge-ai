def execute_actions(actions):

    results = []

    for a in actions:

        if a == "Trigger emergency procurement":
            results.append({"action": a, "status": "FAILED"})
        else:
            results.append({"action": a, "status": "SUCCESS"})

    return results