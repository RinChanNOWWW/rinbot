import json
from typing import Any, Dict


def deserialize(data: str) -> dict:
    """
    Given a string, deserialize it from JSON.
    """
    if data is None:
        return {}

    def fix(jd: Any) -> Any:
        if type(jd) == dict:
            # Fix each element in the dictionary.
            for key in jd:
                jd[key] = fix(jd[key])
            return jd

        if type(jd) == list:
            # Could be serialized by us, could be a normal list.
            if len(jd) >= 1 and jd[0] == "__bytes__":
                # This is a serialized bytestring
                return bytes(jd[1:])

            # Possibly one of these is a dictionary/list/serialized.
            for i in range(len(jd)):
                jd[i] = fix(jd[i])
            return jd

        # Normal value, its deserialized version is itself.
        return jd

    return fix(json.loads(data))
