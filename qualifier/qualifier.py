from PIL import Image


def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    if image_size[0] % tile_size[0] or image_size[1] % tile_size[1]:
        # returns False if tile ratio doesn't fit the image size
        return False

    if len(ordering) != len(set(ordering)):
        # returns False if tiles are used more than once
        return False

    num_tiles = (image_size[0] * image_size[1]) / (tile_size[0] * tile_size[1])
    if not num_tiles.is_integer():
        # returns False if the number of tiles is not a whole number
        return False

    if num_tiles != len(ordering):
        return False

    for i in range(int(num_tiles)):
        if i not in ordering:
            # returns False if a tile is not used
            return False

    return True


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    img = Image.open(image_path)
    image_size = img.size
    if not valid_input(image_size, tile_size, ordering):
        raise ValueError('The tile size or ordering are not valid for the given image')

    tiles = dict()
    num_tiles = (int(image_size[0] / tile_size[0]),  # number of tiles in direction x and y
                 int(image_size[1] / tile_size[1]))
    for y in range(num_tiles[1]):
        for x in range(num_tiles[0]):
            x0, y0, x1, y1 = (tile_size[0] * x, tile_size[1] * y,
                              tile_size[0] * (x + 1), tile_size[1] * (y + 1))
            tiles[(x0, y0)] = img.crop((x0, y0, x1, y1))

    new_image = Image.new(mode=img.mode, size=image_size)
    for target_pos, actual_pos in enumerate(ordering):
        new_image.paste(tiles[list(tiles.keys())[actual_pos]], list(tiles.keys())[target_pos])

    new_image.save(out_path)
