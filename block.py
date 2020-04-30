class Block:
    def __init__(self, attributes):
        self.attributes = attributes

    def __eq__(self, other):
        if self is None or other is None:
            return False
        for attribute in self.attributes:
            if self.attributes[attribute] != other.attributes[attribute]:
                return False
        return True

    def __repr__(self):
        return "Block({})".format(self.attributes)

    def get_attribute_value(self, attribute):
        try:
            return self.attributes[attribute]
        except KeyError:
            return False
