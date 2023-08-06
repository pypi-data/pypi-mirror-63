import json


class JSONParsable:
    """
    A class representing an object that can be parsed from a JSON dictionary. Overriding the parsing_keys property
    allows easy mapping from the JSON dictionary keys to the objects properties.
    For example having:

    parsing_keys = {
        "name": "title"
    }

    will store the value from the JSON dictionary key "name" in the object's title property.

    Attributes
    ----------
    parsing_keys : dict
        The keys to map from JSON to object properties
    """
    parsing_keys = {}

    def __init__(self, **entries):
        for entry_key, value in entries.items():
            # Check if another key is specified in parsing keys, else fall back on the entry_key value
            key = self.parsing_keys.get(entry_key, entry_key)

            try:
                # Make sure the property name exists, else skip the value
                getattr(self, key)

                # Set the value for entry_key as property on self
                setattr(self, key, value)
            except AttributeError:
                # getattr raised an AttributeError, continue with the next value
                continue

    def to_dictionary(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.to_dictionary(),
                          sort_keys=True, indent=4)
