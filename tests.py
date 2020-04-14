import block_model_proccesor

def test_load_model():
    return block_model_proccesor.load_block_file("D:\\202001\\Software\\project\\group_1_2020\\mclaughlin_limit.blocks")

def test_answer():
    assert test_load_model() == True
