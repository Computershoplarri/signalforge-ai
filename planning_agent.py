def generate_plan(risk):

    if risk >= 3:
        return [
            "Validate inventory",
            "Trigger emergency procurement",
            "Notify logistics team",
            "Update customers",
            "Start monitoring"
        ]

    return ["Monitor system"]