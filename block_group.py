from block import Block

class BlockGroup:
    def __init__(self, list_of_blocks, x_offset, y_offset, z_offset, new_id, mass_column):
        self.blocks = list_of_blocks
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
        self.new_id = new_id
        self.mass_column = mass_column

    def convert_to_block(self, continuous_attributes, proportional_attributes, categorical_attributes):
        new_x = ((self.blocks[0]["x"] -  self.x_offset) // len(self.blocks)) + self.x_offset
        new_y = ((self.blocks[0]["y"] -  self.y_offset) // len(self.blocks)) + self.y_offset
        new_z = ((self.blocks[0]["z"] -  self.z_offset) // len(self.blocks)) + self.z_offset
        new_attributes = {"id": self.new_id, "x": new_x, "y": new_y, "z": new_z}

        for attribute in continuous_attributes:
            new_attributes[attribute] = sum([b[attribute] for b in self.blocks])
        for attribute, unit in proportional_attributes:
            if unit == "percentage":
                new_attributes[attribute] = sum(b[self.mass_column] * b[attribute] for b in self.blocks) / \
                                            sum(b[self.mass_column] for b in self.blocks)
            elif unit == "ppm":
                new_attributes[attribute] = sum(b[self.mass_column] * (b[attribute]/10000) for b in self.blocks) / \
                                            sum(b[self.mass_column] for b in self.blocks)
            elif unit == "oz_per_ton":
                new_attributes[attribute] = sum(b[self.mass_column] * (b[attribute] * 0.00342853) for b in self.blocks) / \
                                            sum(b[self.mass_column] for b in self.blocks)
            elif unit == "proportion":
                new_attributes[attribute] = sum(b[self.mass_column] * (b[attribute] * 100) for b in self.blocks) / \
                                            sum(b[self.mass_column] for b in self.blocks)
        for attribute in categorical_attributes:
            values = [b[attribute] for b in self.blocks]
            new_attributes[attribute] = max(set(values), key=values.count)

        return Block(new_attributes)