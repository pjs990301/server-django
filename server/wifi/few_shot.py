import torch
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm
from .util import extract_test_sample

def test(model, test_x, test_y, n_way, n_support, n_query, test_episode, device):
    """
    Tests the protonet
    Args:
        model: trained models
        test_x (np.array): dataloader dataframes of testing set
        test_y (np.array): labels of testing set
        n_way (int): number of classes in a classification task
        n_support (int): number of labeled examples per class in the support set
        n_query (int): number of labeled examples per class in the query set
        test_episode (int): number of episodes to test on
    """
    model = model.to(device)
    conf_mat = torch.zeros(n_way, n_way)
    running_loss = 0.0
    running_acc = 0.0

    total_correct_predictions = 0
    total_predictions = 0

    '''
    Modified
    # Extract sample just once
    '''
    sample = extract_test_sample(n_way, n_support, n_query, test_x, test_y)
    query_samples = sample['q_csi_mats']

    # Create target domain Prototype Network with support set(target domain)
    z_proto = model.create_protoNet(sample)
    total_count = 0
    model.eval()
    with torch.no_grad():
        for episode in tqdm(range(test_episode), desc="test"):
            for label, q_samples in enumerate(query_samples):
                for i in range(0, len(q_samples) // n_way):
                    output = model.proto_test(q_samples[i * n_way:(i + 1) * n_way], z_proto, n_way, label)
                    # print(output)
                    
                    pred_labels = output['y_hat'].cpu().int().squeeze()  # assuming output has shape (n_way, 1)
                    total_predictions += pred_labels.shape[0]
                    total_correct_predictions += (pred_labels == label).sum().item()

                    # populate the confusion matrix
                    for pred_label in pred_labels:
                        conf_mat[label, pred_label.item()] += 1

                    running_acc += output['acc']
                    total_count += 1
        print(conf_mat)
    if total_count == 0:
        avg_acc = 0
    else :
        avg_acc = running_acc / total_count
    print('Test results -- Acc: {:.5f}'.format(avg_acc))
    return (conf_mat / (test_episode * n_query), avg_acc)
