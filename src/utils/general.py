

def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True

class Struct:
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Struct(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Struct(b) if isinstance(b, dict) else b)