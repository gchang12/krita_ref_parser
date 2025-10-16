"""
Determines which images are unneeded, and performs image-related manipulations.
"""

from PIL import Image

SOURCE_DIR = "../../input/docs-krita-org/_build/html/_images/"
TARGET_DIR = "../../output/images/"

def halve_image(filename: str, *, get_first_half: bool):
    """
    Returns one of two halves of image specified by `filename`.
    """
    #logger.debug("Now halving: %s", filename)
    with Image.open(filename) as img:
        half_width = int(img.size[0] / 2)
        full_height = img.size[1]
        full_width = img.size[0]
        # (top, left, right, bottom)
        if get_first_half:
            box = (0, 0, half_width, full_height)
        else:
            box = (half_width, 0, full_width, full_height)
        half_image = img.crop(box)
    return half_image

def halve_blendingmode_dots_images(og_dots_image, imagedir):
    """
    Produces collection of dot-images by blending mode.
    """
    for imagefile in Path(imagedir).iterdir():
        if not str(imagefile).endswith("_with_dots.png"):
            continue
        if imagefile.name == og_dots_image:
            continue
        if not Path(imagedir, og_dots_image).exists():
            og_image = halve_image(imagefile, get_first_half=True)
            og_image.save('/'.join([imagedir, og_dots_image]))
        blended_image = halve_image(imagefile, get_first_half=False)
        blended_image.save(imagefile)

# delete unused images
def delete_unused_images(excerptdir_root, imagedir_root, og_dots_image, index_name):
    """
    Deletes images that are not referenced by the compiled HTML files.
    """
    #used_images = set()
    with open(index_name, encoding="utf-8") as rfile:
        index = json.load(rfile)
    used_images = set(Path(record['icon']).name for record in index if record['icon'] is not None)
    for excerpt_dir in Path(excerptdir_root).iterdir():
        for excerpt_file in excerpt_dir.iterdir():
            with open(excerpt_file, encoding="utf-8") as rfile:
                soup = BeautifulSoup(rfile, "html.parser")
            for img in soup.find_all('img'):
                img_src = Path(img['src']).name
                used_images.add(img_src)
    for imagefile in Path(imagedir_root).iterdir():
        if imagefile.name == og_dots_image:
            continue
        if imagefile.is_dir():
            continue
        if imagefile.name in used_images:
            continue
        imagefile.unlink()

def transfer_images(root, imagedir_root):
    """
    Copies all images from source to output.
    """
    #os.chmod(imagedir_root, 0o555)
    for imagefile in Path(root, "..", "_images").iterdir():
        shutil.copyfile(imagefile, Path(imagedir_root, imagefile.name))

if __name__ == "__main__":
    filename = "images/.test.png"
    half_image = halve_image(filename, get_first_half=False)

