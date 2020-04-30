from block_group import BlockGroup
from block import Block

class BlockModel:
    def __init__(self, name, blocks, columns, minerals):
        self.name = name
        self.blocks = blocks
        self.columns = columns
        self.minerals = minerals

    def __eq__(self, other):
        for i in range(len(self.blocks)):
            if self.blocks[i] != other.blocks[i]:
                return False
        if self.columns != other.columns:
            return False
        if self.minerals != other.minerals:
            return False
        return True

    def __repr__(self):
        return "BlockModel({}, {}, {}, {})".format(self.name, self.blocks, self.columns, self.minerals)

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
        new_list = []
        for i in matrix:
            for j in i:
                for k in j:
                    print("k:", k)
                    new_list.append(k)
        return sorted(new_list, key=lambda block: block.attributes["id"])
        #return sorted([matrix[i][j][k] for k in range(len(matrix[0][0])) for j in range(len(matrix[0])) for i in range(len(matrix))], key=lambda block: block.attributes["id"])

    def get_matrix_three_d_from_blocks_list_including_air_blocks(self, rx, ry, rz):
        max_x = self.get_max_coordinate("x")
        max_x += len(range(max_x + 1)) % rx + 1
        max_y = self.get_max_coordinate("y")
        max_y += len(range(max_y + 1)) % ry + 1
        max_z = self.get_max_coordinate("z")
        max_z += len(range(max_z + 1)) % rz + 1
        print("maximos:", max_x, max_y, max_z)
        x_offset = self.get_offset("x")
        y_offset = self.get_offset("y")
        z_offset = self.get_offset("z")
        matrix = []
        for i in range(x_offset, max_x):
            matrix.append([])
            for j in range(y_offset, max_y):
                matrix[i - x_offset].append([])
                for k in range(z_offset, max_z):
                    # print(i, j, k)

                    # matrix[i - x_offset][j - y_offset].append("")
                    block = self.get_block_by_coordinates(i, j, k)
                    if  block is None:
                        block_attributes = {"id": -1, "x": i, "y": j, "z": k}
                        for column in self.columns[4:]:
                            block_attributes[column] = 0
                        matrix[i - x_offset][j - y_offset].append(Block(block_attributes))
                    else:
                        matrix[i - x_offset][j - y_offset].append(block)
        return matrix

    def get_max_coordinate(self, coordinate):
        return max([block.attributes[coordinate] for block in self.blocks])

    def get_offset(self, coordinate):
        return min([block.attributes[coordinate] for block in self.blocks])

    def reblock(self, rx, ry, rz, continuous_attributes, proportional_attributes, categorical_attributes, mass_columns):
        blocks_matrix = self.get_matrix_three_d_from_blocks_list_including_air_blocks(rx, ry, rz)
        new_x_length = len(blocks_matrix) // rx if float(len(blocks_matrix) // rx) == len(blocks_matrix) / rx else len(blocks_matrix) // rx + 1
        new_y_length = 0 if new_x_length == 0 else (len(blocks_matrix[0]) // ry if float(len(blocks_matrix[0]) // ry) == len(blocks_matrix[0]) / ry else len(blocks_matrix[0]) // ry + 1)
        new_z_length = 0 if new_y_length == 0 else (len(blocks_matrix[0][0]) // rz if float(len(blocks_matrix[0][0]) // rz) == len(blocks_matrix[0][0]) / rz else len(blocks_matrix[0][0]) // rz + 1)
        print("new dimensions:", new_x_length, new_y_length, new_z_length)
        new_blocks = self.get_new_empty_blocks(new_x_length, new_y_length, new_z_length)
        x_offset = self.get_offset("x")
        y_offset = self.get_offset("y")
        z_offset = self.get_offset("z")
        new_i = 0
        new_id = 0
        print("largos:", len(blocks_matrix), len(blocks_matrix[0]), len(blocks_matrix[0][0]))
        for i in range(x_offset, len(blocks_matrix) + x_offset, rx):
            new_j = 0
            for j in range(y_offset, len(blocks_matrix[0]) + y_offset, ry):
                new_k = 0
                for k in range(z_offset, len(blocks_matrix[0][0]) + z_offset, rz):
                    # new = self.get_reblock_coming_from_group_of_blocks(i, j, k, rx, ry, rz, new_id, x_offset, y_offset, z_offset,
                    #                                                                                continuous_attributes, proportional_attributes,
                    #                                                                                categorical_attributes, mass_columns, blocks_matrix)
                    # #print("new:", new.attributes)
                    # new_blocks[new_i][new_j][new_k] = new
                    print(i, j , k, " ---> ", new_i, new_j, new_k)
                    new_id += 1
                    new_k += 1
                new_j += 1
            new_i += 1
        for a in new_blocks:
            for b in a:
                to_remove = b.count(None)
                # print(to_remove)
                for c in range(to_remove):
                    b.remove(None)
        # blocks_to_remove = []
        # for block in new_blocks:
        #     if block is None:
        #         blocks_to_remove.append(block)
        # for block in blocks_to_remove:
        #     new_blocks.remove(block)
        list_of_blocks = self.get_list_of_blocks_coming_from_matrix_three_d(new_blocks)

        new_block_model = BlockModel(name="{}_reblocked_{}_{}_{}".format(self.name, rx, ry, rz), blocks=list_of_blocks, columns=self.columns, minerals=self.minerals)
        return new_block_model

    def get_new_empty_blocks(self, new_x_length, new_y_length, new_z_length):
        return [[[None for k in range(new_z_length)] for j in range(new_y_length)] for i in range(new_x_length)]

    def get_reblock_coming_from_group_of_blocks(self, first_block_x_index, first_block_y_index, first_block_z_index, rx, ry, rz,
                                                new_id, x_offset, y_offset, z_offset, continuous_attributes, proportional_attributes,
                                                categorical_attributes, mass_columns, blocks_matrix):
        group = []
        for a in range(first_block_x_index, first_block_x_index + rx):
            for b in range(first_block_y_index, first_block_y_index + ry):
                for c in range(first_block_z_index, first_block_z_index + rz):
                    print("append to group:", a, b, c)
                    group.append(blocks_matrix[a][b][c])
                    # print("append to group:", a - x_offset, b - y_offset, c - z_offset)
                    # group.append(blocks_matrix[a - x_offset][b - y_offset][c - z_offset])
        # if len(group) == 1:
        #     return group[0]
        # else:
        new_block_group = BlockGroup(group, x_offset, y_offset, z_offset, new_id, mass_columns, rx, ry, rz)
        return new_block_group.convert_to_block(continuous_attributes, proportional_attributes, categorical_attributes)