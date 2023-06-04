import io
import logging
from pathlib import Path
from typing import Iterator, Union


from openpecha.buda import api as buda_api
from PIL import Image as PillowImage
from wand.image import Image as WandImage

from openpecha.utils import dump_yaml, load_yaml


def save_img_with_wand(fp: io.BytesIO, fn: Path) -> bool:
    try:
        with WandImage(blob=fp.getvalue()) as img:
            img.format = "png"
            img.transform_colorspace("gray")
            threshold = 0.5  # Adjust this threshold value as per your needs
            img.threshold(threshold)
            img.save(filename=str(fn))
            return True
    except Exception:
        logging.exception(f"Failed to save {fn} with `Wand`")
        return False

def save_img_with_pillow(fp: io.BytesIO, fn: Path) -> bool:
    """
    uses pillow to interpret the bits as an image and save as a format
    that is appropriate for Google Vision (png instead of tiff for instance).
    """
    try:
        img = PillowImage.open(fp)
        image_gray = img.convert("L")

        # Step 3: Binarize the image
        threshold = 128  # Adjust this threshold value as per your needs
        image_binarized = image_gray.point(lambda x: 0 if x < threshold else 255, "1")
        image_binarized.save(str(fn))
    except Exception:
        logging.exception(f"Failed to save {fn} with `Pillow`")
        return False

    return True

def save_img(fp: io.BytesIO, fn: Union[str, Path], work_dir: Path):
    """Save the image in .png format to `img_groupdir/fn

    Google Vision API does not support bdrc tiff images.

    Args:
        fp (io.BytesIO): image bits
        fn (str): filename
        img_group_dir (Path): directory to save the image
    """
    output_fn = work_dir / fn
    fn = Path(fn)
    if fn.suffix in [".tif", ".tiff", ".TIF"]:
        output_fn = work_dir / f"{fn.stem}.png"

    saved = save_img_with_pillow(fp, output_fn)
    if not saved:
        save_img_with_wand(fp, output_fn)

def save_sample_image(scan_id, img_grp, sample_img_dir):
    imgs = buda_api.get_image_list_s3(scan_id, img_grp)
    s3_folder_prefix = buda_api.get_s3_folder_prefix(scan_id, img_grp)
    sample_img = imgs[len(imgs)//2]
    img_fn = sample_img['filename']
    img_path_s3 = Path(s3_folder_prefix) / img_fn
    img_bits = buda_api.gets3blob(str(img_path_s3))
    if img_bits:
        save_img(img_bits, img_fn, sample_img_dir)

def sample_images(scan_id, img_grp_list, sample_img_dir):

    for img_grp_id, img_grp in img_grp_list.items():
        save_sample_image(scan_id, img_grp_id, sample_img_dir)
        break



if __name__ == "__main__":
    work_catalog = load_yaml(Path('./data/wooden_print_work_catalog.yml'))
    sample_img_dir = Path('./data/sample_images')
    for work_id, img_grp_list in work_catalog.items():
        sample_images(work_id, img_grp_list, sample_img_dir)
