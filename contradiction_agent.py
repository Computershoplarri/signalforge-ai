def detect_conflict(supplier, complaints):

    conflict = "stable" in supplier and ("delayed" in complaints or "unavailable" in complaints)

    return {
        "conflict": conflict,
        "reason": "Supplier vs complaints mismatch detected"
    }