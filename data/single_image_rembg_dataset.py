from data.base_dataset import BaseDataset, get_transform
from data.image_folder import make_dataset
from PIL import Image, ImageFile
from rembg import bg
import numpy as np
import io

ImageFile.LOAD_TRUNCATED_IMAGES = True

class SingleImageRembgDataset(BaseDataset):

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)
        self.A_paths = [opt.input_image_path]
        input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.transform = get_transform(opt, grayscale=(input_nc == 1))

    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index - - a random integer for data indexing

        Returns a dictionary that contains A and A_paths
            A(tensor) - - an image in one domain
            A_paths(str) - - the path of the image
        """
        A_path = self.A_paths[index]
        f = np.fromfile(A_path)
        f_removed_bg = bg.remove(f)
        A_img_transparent_bg = Image.open(io.BytesIO(f_removed_bg)).convert('RGBA')
        A_img = Image.new("RGBA", A_img_transparent_bg.size, "WHITE")
        A_img.paste(A_img_transparent_bg, (0, 0), A_img_transparent_bg)
        A_img = A_img.convert('RGB')
        A = self.transform(A_img)
        return {'A': A, 'A_paths': A_path}

    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.A_paths)
