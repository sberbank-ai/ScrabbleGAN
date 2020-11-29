from config import Config
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
from data_loader.data_generator import CustomDataset
from generate_images import ImgGenerator
from tqdm import tqdm


def calculate_fid(checkpt_path, num_images=25000):
    """
    :param checkpt_path: Path of the model checkpoint file to be used
    :param num_images: Number of images from real and fake images to be taken for consideration
    :return: fid score
    """
    config = Config
    path = './fid_calc/'
    fake_path = path + '/fake/'
    real_path = path + '/real/'
    # Create directories for saving fake and real images
    os.makedirs(fake_path, exist_ok=True)
    os.makedirs(real_path, exist_ok=True)

    # fake images
    print('Generating and saving fake images')
    generator = ImgGenerator(checkpt_path=checkpt_path, config=config)

    # save these fake images
    for idx, img in enumerate(tqdm(range(num_images))):
        # to avoid padding, generate image separately
        img, word_labels = generator.generate(1)
        plt.imshow(img[0], cmap='gray')
        plt.savefig(f'{fake_path}/{idx}.png')

    # real images
    print('Sampling and saving real images')
    dataset = CustomDataset(config)
    # choose random images
    imgs_idx = np.random.choice(len(dataset), num_images)
    for idx in tqdm(imgs_idx):
        w_id = dataset.idx_to_id[idx]
        # Get image
        _, img = dataset.word_data[w_id]
        plt.imshow(img, cmap='gray')
        plt.savefig(f'{real_path}/{idx}.png')

    # calculate fid
    os.system(f'python -m pytorch_fid {real_path} {fake_path}')


if __name__ == "__main__":
    # Construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--checkpt_path", required=True, type=str,
                    help="Path of the model checkpoint file to be used")
    ap.add_argument("-n", "--num_imgs", required=False, type=int,
                    help="number of sample points")
    args = vars(ap.parse_args())
    checkpoint_path = args['checkpt_path']
    num_imgs = args['num_imgs'] if args['num_imgs'] is not None else 25000

    calculate_fid(checkpoint_path, num_imgs)
