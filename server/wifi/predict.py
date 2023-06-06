from .util import * 
from .few_shot import test
import torch
import numpy as np
import random
from proto import load_protonet_vit
# from .config import param

''' 
fix seed
'''
torch.manual_seed(0)
np.random.seed(0)
random.seed(0)


def predict_result(dir_name) :
    # print(dir_name)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    test_x, test_y = load_only_testset(dir_name)
    # print(test_x.shape)
    model = load_protonet_vit(
        in_channels=1,
        patch_size=[16, 64],
        embed_dim=64,
        num_layers=12,
        num_heads=8,
        mlp_dim=4,
        num_classes=4,
        in_size=[64, 64]
    )
    model = model.to(device)
    model = torch.load('/home/jisung/Project/MoWA/server-django/server/wifi/model.pt')
    # print(model)
    conf_mat, test_acc = test(
        model=model,
        test_x=test_x,
        test_y=test_y,
        # n_way=param['test_way'],
        # n_support=param['test_support'],
        # n_query=param['test_query'],
        n_way=2,
        n_support=5,
        n_query=5,
        test_episode=1,
        device = device
    )
    # print(conf_mat, test_acc)
    conf_mat = np.array(conf_mat)  # Convert to NumPy array
    column_sums = np.sum(conf_mat, axis=0)

    max_index = np.argmax(column_sums)

    # test_labels = np.array(['Empty', 'Lying', 'Sitting', 'Standing', 'Walking'])  # Convert to NumPy array
    test_labels = np.array(['input', 'Empty'])  # Convert to NumPy array
    max_value = test_labels[max_index]

    # print(max_value)
    return "fall"