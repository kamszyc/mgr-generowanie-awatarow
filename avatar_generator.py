import os
from options.test_options import TestOptions
from options.test_options_cut import TestOptionsCUT
from data import create_dataset
from models import create_model
from util import util
from PIL import Image, ImageFile
from neural_style_transfer import style_transfer_generate_image
from rembg import bg
import numpy as np
import io

ImageFile.LOAD_TRUNCATED_IMAGES = True

def generate_avatar(method, input_image_path, selected_mode):
    if method == "CycleGAN":
        return generate_avatar_cyclegan(input_image_path, selected_mode)
    elif method == "CycleGAN + pix2pix":
        return generate_avatar_pix2pix(input_image_path, "CycleGAN_pix2pix", 200, selected_mode)
    elif method == "AttentionGAN":
        return generate_avatar_attentiongan(input_image_path, selected_mode)
    elif method == "AttentionGAN + pix2pix":
        return generate_avatar_pix2pix(input_image_path, "AttentionGAN_pix2pix", 150, selected_mode)
    elif method == "CUT (light skin, brown hair)":
        return generate_avatar_cut(input_image_path, 69, selected_mode)
    elif method == "CUT (light skin, black hair)":
        return generate_avatar_cut(input_image_path, 70, selected_mode)
    elif method == "CUT (light skin, blond hair)":
        return generate_avatar_cut(input_image_path, 72, selected_mode)
    elif method == "CUT (dark skin, black hair)":
        return generate_avatar_cut(input_image_path, 73, selected_mode)
    elif method == "Neural style transfer (AttentionGAN style)":
        return generate_avatar_neural_style_transfer(input_image_path, generate_avatar_attentiongan, selected_mode)
    else:
        raise Exception("Unsupported method")

def generate_avatar_cyclegan(input_image_path, selected_mode):
    testoptions = TestOptions()
    testoptions.default_gpu_id = get_gpu_id(selected_mode)
    opt = testoptions.parse()
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
    opt.dataset_mode = "single_image_rembg"
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

def generate_avatar_attentiongan(input_image_path, selected_mode):
    testoptions = TestOptions()
    testoptions.default_gpu_id = get_gpu_id(selected_mode)
    opt = testoptions.parse()
    # --name celeba_bitmoji_attentiongan_small_filtered_white_bg 
    # --model attention_gan --dataset_mode unaligned --norm instance --phase test 
    # --no_dropout --load_size 256 --crop_size 256 --batch_size 1 --gpu_ids 0 --saveDisk  --num_test 200 --epoch 45
    
    opt.model = "attention_gan"
    opt.phase = "test"
    opt.name = "AttentionGAN"
    opt.epoch = 45
    opt.no_dropout = True
    opt.norm = "instance"
    opt.crop_size = 256
    opt.num_threads = 0   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    opt.dataroot = ""
    opt.dataset_mode = "single_image_rembg"
    opt.saveDisk = True
    opt.input_image_path = input_image_path
    opt.only_generate_fake_B = True
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers

    if opt.eval:
        model.eval()
    data = next(iter(dataset))
    model.set_input(data)  # unpack data from data loader
    model.test()           # run inference
    visuals = model.get_current_visuals()
    im_data = visuals["fake_B"]
    im = util.tensor2im(im_data)
    return Image.fromarray(im.astype('uint8'), 'RGB')


def generate_avatar_pix2pix(input_image_path, name, epoch, selected_mode):
    testoptions = TestOptions()
    testoptions.default_gpu_id = get_gpu_id(selected_mode)
    opt = testoptions.parse()
    opt.model = "pix2pix"
    opt.phase = "test"
    opt.name = name
    opt.epoch = epoch
    opt.no_dropout = True
    opt.netG = "unet_256"
    opt.direction = "AtoB"
    opt.norm = "batch"
    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 0
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    opt.dataroot = ""
    opt.dataset_mode = "single_image_rembg"
    opt.input_image_path = input_image_path
    opt.only_generate_fake_B = True
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers

    if opt.eval:
        model.eval()
    data = next(iter(dataset))
    model.set_input(data)  # unpack data from data loader
    model.test()           # run inference
    visuals = model.get_current_visuals()
    im_data = visuals["fake_B"]
    im = util.tensor2im(im_data)
    return Image.fromarray(im.astype('uint8'), 'RGB')


def generate_avatar_cut(input_image_path, epoch, selected_mode):
    testoptions = TestOptionsCUT()
    testoptions.default_gpu_id = get_gpu_id(selected_mode)
    opt = testoptions.parse()
    opt.model = "cut"
    opt.phase = "test"
    opt.name = "CUT"
    opt.CUT_mode = "CUT"
    opt.epoch = epoch

    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    opt.load_iter = 0
    opt.dataroot = ""
    opt.dataset_mode = "single_image_rembg"
    opt.input_image_path = input_image_path
    opt.only_generate_fake_B = True
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)      # create a model given opt.model and other options

    data = next(iter(dataset))
    model.data_dependent_initialize(data)
    model.setup(opt)               # regular setup: load and print networks; create schedulers
    #model.parallelize()
    if opt.eval:
        model.eval()

    model.set_input(data)  # unpack data from data loader
    model.test()           # run inference
    visuals = model.get_current_visuals()
    im_data = visuals["fake_B"]
    im = util.tensor2im(im_data)
    return Image.fromarray(im.astype('uint8'), 'RGB')

def generate_avatar_neural_style_transfer(input_image_path, generate_style_func, selected_mode):
    f = np.fromfile(input_image_path)
    f_removed_bg = bg.remove(f)
    content_img_transparent_bg = Image.open(io.BytesIO(f_removed_bg)).convert('RGBA')
    content_img = Image.new("RGBA", content_img_transparent_bg.size, "WHITE")
    content_img.paste(content_img_transparent_bg, (0, 0), content_img_transparent_bg)
    content_img = content_img.convert('RGB')

    style_img = generate_style_func(input_image_path, selected_mode)
    return style_transfer_generate_image(content_img, style_img, selected_mode)

def get_gpu_id(selected_mode):
    if selected_mode == 'cuda':
        return '0'
    else:
        return '-1'
