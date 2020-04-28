class BlockModel:
    def __init__(self, name, blocks, columns, minerals):
        self.name = name
        self.blocks = blocks
        self.columns = columns
        self.minerals = minerals

    def get_number_of_blocks(self):
        return len(self.blocks)

    def get_blocks_range(self, from_id, to_id):
        blocks = list(filter(lambda block: from_id <= block.attributes["id"] <= to_id, self.blocks))
        return blocks

    def get_block_by_coordinates(self, x, y, z):
        block = list(filter(lambda b: b.attributes["x"] == int(x) and b.attributes["y"] == int(y) and b.attributes["z"] == int(z), self.blocks))
        if len(block) == 0:
            return False
        else:
            return block[0]
