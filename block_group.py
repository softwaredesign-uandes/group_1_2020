from reblockable import Reblockable
from block import Block

class BlockGroup(Reblockable):
    def __init__(self, list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz, continuous_attributes, proportional_attributes, categorical_attributes):
        self.blocks = list_of_blocks
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
        self.new_id = new_id
        self.mass_columns = mass_columns
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.continuous_attributes = continuous_attributes
        self.proportional_attributes = proportional_attributes
        self.categorical_attributes = categorical_attributes
        self.get_new_attributes()

    def get_new_attributes(self):
        new_x = ((self.blocks[0].attributes["x"] - self.x_offset) // self.rx) + self.x_offset
        new_y = ((self.blocks[0].attributes["y"] - self.y_offset) // self.ry) + self.y_offset
        new_z = ((self.blocks[0].attributes["z"] - self.z_offset) // self.rz) + self.z_offset
        # print("new coordenates:", new_x, new_y, new_z)
        new_attributes = {"id": self.new_id, "x": new_x, "y": new_y, "z": new_z}
        for attribute in self.continuous_attributes:
            new_attributes[attribute] = sum([b.attributes[attribute] for b in self.blocks])
        for attr, unit in self.proportional_attributes.items():
            denominator = sum(sum([b.attributes[m] for m in self.mass_columns]) for b in self.blocks)
            if denominator == 0:
                denominator = 1
            if unit == "percentage":
                new_attributes[attr] = sum(sum([b.attributes[m] for m in self.mass_columns]) * b.attributes[attr] for b in self.blocks) / denominator
            elif unit == "ppm":
                new_attributes[attr] = sum(sum([b.attributes[m] for m in self.mass_columns]) * (b.attributes[attr]/10000) for b in self.blocks) / denominator
            elif unit == "oz_per_ton":
                new_attributes[attr] = sum(sum([b.attributes[m] for m in self.mass_columns]) * (b.attributes[attr] * 0.00342853) for b in self.blocks) / denominator
            elif unit == "proportion":
                new_attributes[attr] = sum(sum([b.attributes[m] for m in self.mass_columns]) * (b.attributes[attr] * 100) for b in self.blocks) / denominator
        for at in self.categorical_attributes:
            values = [b.attributes[at] for b in self.blocks]
            new_attributes[at] = max(set(values), key=values.count)
        self.attributes = new_attributes
        # return Block(new_attributes)

    def __eq__(self, other):
        if self is None or other is None:
            return False
        for attribute in self.attributes:
            if self.attributes[attribute] != other.attributes[attribute]:
                return False
        for attribute in other.attributes:
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