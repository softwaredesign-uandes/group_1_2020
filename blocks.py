class Block:
    def __init__(self, attributes):
        self.attributes = attributes

    def get_attribute_value(self, attribute):
        try:
            return self.attributes[attribute]
        except KeyError:
            return False
