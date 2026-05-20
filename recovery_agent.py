def recover(results):

    recovery = []

    for r in results:
        if r["status"] == "FAILED":
            recovery.append("Fallback supplier activated")

    return recovery