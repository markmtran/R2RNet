import os
import argparse
from glob import glob
from model import R2RNet
import torch

parser = argparse.ArgumentParser(description='')
device = torch.device('cuda:0')
parser.add_argument('--gpu_id', dest='gpu_id', 
                    default="0",
                    help='GPU ID (-1 for CPU)')
parser.add_argument('--data_dir', dest='data_dir',
                    default='/content/data/eval15/low',
                    help='directory storing the test data')
parser.add_argument('--ckpt_dir', dest='ckpt_dir', 
                    default='/content/R2RNet/ckpts/',
                    help='directory for checkpoints')
parser.add_argument('--res_dir', dest='res_dir', 
                    default='/content/test_results_r2rnet',
                    help='directory for saving the results')

args = parser.parse_args()


def predict(model):

    test_low_data_names  = glob(args.data_dir + '/' + '*.*')
    test_low_data_names.sort()
    print('Number of evaluation images: %d' % len(test_low_data_names))

    model.predict(test_low_data_names,
                res_dir=args.res_dir,
                ckpt_dir=args.ckpt_dir)


if __name__ == '__main__':
    if args.gpu_id != "-1":
        # Create directories for saving the results
        if not os.path.exists(args.res_dir):
            os.makedirs(args.res_dir)
        # Setup the CUDA env
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_id
        # Create the model
        with torch.no_grad():
            model = R2RNet().to(device)
            # Test the model
            predict(model)
    else:
        # CPU mode not supported at the moment!
        raise NotImplementedError
