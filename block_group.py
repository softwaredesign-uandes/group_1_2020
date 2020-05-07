from block import Block

class BlockGroup:
    def __init__(self, list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz):
        self.blocks = list_of_blocks
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
        self.new_id = new_id
        self.mass_columns = mass_columns
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def convert_to_block(self, continuous_attributes, proportional_attributes, categorical_attributes):
        new_x = ((self.blocks[0].attributes["x"] - self.x_offset) // self.rx) + self.x_offset
        new_y = ((self.blocks[0].attributes["y"] - self.y_offset) // self.ry) + self.y_offset
        new_z = ((self.blocks[0].attributes["z"] - self.z_offset) // self.rz) + self.z_offset
        new_attributes = {"id": self.new_id, "x": new_x, "y": new_y, "z": new_z}
        for attribute in continuous_attributes:
            new_attributes[attribute] = sum([b.attributes[attribute] for b in self.blocks])
        for attr, unit in proportional_attributes.items():
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
        for at in categorical_attributes:
            values = [b.attributes[at] for b in self.blocks]
            new_attributes[at] = max(set(values), key=values.count)
        return Block(new_attributes)