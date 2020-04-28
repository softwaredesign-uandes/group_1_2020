from block_group import BlockGroup
from block import Block

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
        block = list(filter(lambda b: b.attributes["x"] == int(x) and b.attributes["y"] == int(y)
                                      and b.attributes["z"] == int(z), self.blocks))
        if len(block) == 0:
            return None
        else:
            return block[0]

    def get_list_of_blocks_coming_from_matrix_three_d(self, matrix):
        return sorted([matrix[i][j][k] for k in range(len(matrix[0][0])) for j in range(len(matrix[0])) for i in range(len(matrix))], key=lambda attribute: attribute["id"])

    def get_matrix_three_d_from_blocks_list(self):
        max_x = self.get_max_coordinate("x")
        max_y = self.get_max_coordinate("y")
        max_z = self.get_max_coordinate("z")
        return [[[self.get_block_by_coordinates(i, j, k) for k in range(max_z)] for j in range(max_y)] for i in range(max_x)]

    def get_max_coordinate(self, coordinate):
        return max([block.attributes[coordinate] for block in self.blocks])

    def reblock(self, rx, ry, rz):
        new_x_length = len(self.blocks) // rx
        new_y_length = 0 if new_x_length == 0 else len(self.blocks[0]) // ry
        new_z_length = 0 if new_y_length == 0 else len(self.blocks[0][0]) // rz
        new_blocks = self.get_new_empty_blocks(new_x_length, new_y_length, new_z_length)
        new_i = 0
        for i in range(0, len(self.blocks), rx):
            new_j = 0
            for j in range(0, len(self.blocks[0]), ry):
                new_k = 0
                for k in range(0, len(self.blocks[0][0]), rz):
                    new_blocks[new_i][new_j][new_k] = self.get_reblock_coming_from_group_of_blocks(i, j, k, rx, ry, rz)
                    new_k += 1
                new_j += 1
            new_i += 1
        list_of_blocks = self.get_list_of_blocks_coming_from_matrix_three_d(new_blocks)
        return BlockModel(name="{}_reblocked_{}_{}_{}".format(self.name, rx, ry, rz), blocks=list_of_blocks, columns=self.columns, minerals=self.minerals)

    def get_new_empty_blocks(self, new_x_length, new_y_length, new_z_length):
        return [[[None for k in range(new_z_length)] for j in range(new_y_length)] for i in range(new_x_length)]

    def get_reblock_coming_from_group_of_blocks(self, first_block_x_index, first_block_y_index, first_block_z_index, rx, ry, rz):
        group = []
        for i in range(first_block_x_index, first_block_x_index + rx):
            for j in range(first_block_y_index, first_block_y_index + ry):
                for k in range(first_block_z_index, first_block_z_index + rz):
                    group.append(self.blocks[i][j][k])
        theoretical_number_of_blocks = rx * ry * rz
        real_number_of_blocks = len(group)
        if theoretical_number_of_blocks > real_number_of_blocks:
            group.extend([Block({attribute: 0 for attribute in self.blocks[0].attributes}) for _ in range(theoretical_number_of_blocks - real_number_of_blocks)])
        return group[0] if len(group) == 1 else BlockGroup(group)