TANKS_TO_NOZZLES_MAPPING = {1: [13, 17, 21], 2: [14, 18, 22], 3: [15, 19, 23], 4: [16, 20, 24]}


def get_nozzles_from_tank(tankID):
    if not tankID in TANKS_TO_NOZZLES_MAPPING.keys():
        raise ValueError("Provided tankID is not available")

    return TANKS_TO_NOZZLES_MAPPING[tankID]
