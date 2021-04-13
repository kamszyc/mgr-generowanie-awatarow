import os
from options.test_options import TestOptions
from data import create_dataset
from models import create_model
from util import util
from PIL import Image

def get_cyclegan_output(input_image_path):
    opt = TestOptions().parse()
    opt.model = "test"
    opt.phase = "test"
    opt.name = "CycleGAN"
    opt.epoch = 70
    opt.no_dropout = True
    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 0
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    opt.dataroot = ""
    opt.dataset_mode = "single_image"
    opt.input_image_path = input_image_path
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers

    if opt.eval:
        model.eval()
    data = next(iter(dataset))
    model.set_input(data)  # unpack data from data loader
    model.test()           # run inference
    visuals = model.get_current_visuals()
    im_data = visuals["fake"]
    im = util.tensor2im(im_data)
    return Image.fromarray(im.astype('uint8'), 'RGB')
