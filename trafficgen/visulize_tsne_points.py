import copy
import os
import numpy as np
import torch
from tqdm import tqdm
from sklearn import manifold
from trafficgen.init.utils.init_dataset import WaymoAgent
from trafficgen.traffic_generator.utils.tsne import visualize_tsne_points,visualize_tsne_images
import wandb
from trafficgen.init.model.tg_feature import initializer
from trafficgen.init.utils.init_dataset import InitDataset
from trafficgen.utils.config import load_config_init, get_parsed_args
from trafficgen.utils.utils import setup_seed,wash
from torch.utils.data import DataLoader
from trafficgen.traffic_generator.utils.vis_utils import draw

dataset_to_color = {
    'waymo': 'red',
    'nuplan': 'blue',
    'pg': 'green',
}

if __name__ == "__main__":
    wandb.init(
        project="tsne",
    )
    #vis_num = 4

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    args = get_parsed_args()
    cfg = load_config_init(args.config)

    test_set = InitDataset(cfg)

    data_loader = DataLoader(test_set, batch_size=1, num_workers=0, shuffle=False, drop_last=True)

    model = initializer.load_from_checkpoint('traffic_generator/ckpt/init_sn.ckpt').to(device)

    model.eval()

    datasize = len(data_loader)
    features = torch.zeros([datasize, 1024], device=device)

    ret = {}
    dataset_list = []

    with torch.no_grad():
        for idx, batch in enumerate(tqdm(data_loader)):

            for k in batch:
                try:
                    batch[k] = batch[k].to(device)
                except:
                    pass
            features[idx] = model(batch)
            dataset_list.append(batch['dataset'][0])

    tsne = manifold.TSNE(
        n_components=2,
        init='pca',
        learning_rate='auto',
        n_jobs=-1
    )

    c_list = [dataset_to_color[c] for c in dataset_list]
    Y = tsne.fit_transform(features.numpy())

    ret['tsne_points'] = wandb.Image(visualize_tsne_points(Y,c_list))
    wandb.log(ret)