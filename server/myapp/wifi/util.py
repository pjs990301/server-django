from .dataset import *
from ReWiS_model import *
import torch
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np

def load_meta_data_fewshot(root) :
    print('using dataset: Home DATA Few shot')
    train_x, train_y = dataset.read_csi_csv(root + '/few_shot_datasets/meta',one_file=True)
    train_x = np.expand_dims(train_x, axis=1)
    test_x, test_y = dataset.read_csi_csv(root + '/few_shot_datasets/train_5',one_file=True)
    test_x = np.expand_dims(test_x, axis=1)

    return train_x, train_y, test_x, test_y

def load_only_testset(dir) :
    print()


def euclidean_dist(x, y):
    """
    Computes euclidean distance btw x and y
    Args:
        x (torch.Tensor): shape (n, d). n usually n_way*n_query
        y (torch.Tensor): shape (m, d). m usually n_way
    Returns:
        torch.Tensor: shape(n, m). For each query, the distances to each centroid
    """
    n = x.size(0)
    m = y.size(0)
    d = x.size(1)
    assert d == y.size(1)

    x = x.unsqueeze(1).expand(n, m, d)
    y = y.unsqueeze(0).expand(n, m, d)

    return torch.pow(x - y, 2).sum(2)

def extract_test_sample(n_way, n_support, n_query, datax, datay):
    """
    Picks random sample of size n_support+n_querry, for n_way classes
    Args:
        n_way (int): number of classes in a classification task
        n_support (int): number of labeled examples per class in the support set
        n_query (int): number of labeled examples per class in the query set
        datax (np.array): dataset of csi dataframes
        datay (np.array): dataset of labels
    Returns:
        (dict) of:
          (torch.Tensor): sample of csi dataframes. Size (n_way, n_support+n_query, (dim))
          (int): n_way
          (int): n_support
          (int): n_query
    """
    #K = np.array(['empty', 'jump', 'stand', 'walk']) # ReWis
    K = np.array(param['test_labels'])

    # extract support set & query set
    support_sample = []
    query_sample = []
    for cls in K:
        datax_cls = datax[datay == cls]
        # print(datax_cls.shape)
        # print(datax_cls.dtype)

        support_cls = datax_cls[:n_support]
        query_cls = np.array(datax_cls[n_support:n_support+n_query])

        # print(query_cls.shape)
        # print(query_cls.dtype)
        # print("---------")

        support_sample.append(support_cls)
        query_sample.append(query_cls)
    
    support_sample = np.array(support_sample)
    query_sample = np.array(query_sample)

    # print(support_sample.dtype)
    # print(type(support_sample))

    # print(query_sample.dtype)
    # print(type(query_sample))

    support_sample = torch.from_numpy(support_sample).float()
    query_sample = torch.from_numpy(query_sample).float()

    return ({
        's_csi_mats': support_sample,
        'q_csi_mats': query_sample,
        'n_way': n_way,
        'n_support': n_support,
        'n_query': n_query
    })


if __name__ == "__main__" :
    load_ReWiS_data_split
    input_size = (1,250,90)
    # print(summary(wifi, input_size = input_size))
    print(torchsummary.summary(model, input_size = input_size))