import pygame as pg

def rotate(image, angle):
    """Rotate an image while keeping its center and size"""

    # Get the center of the image
    origin = image.get_rect()

    # Rotate the pygame image
    image_rotation = pg.transform.rotate(image, angle)

    # Rotate the image based on the rect of itself
    rect_rotation = origin.copy()
    rect_rotation.center = image_rotation.get_rect().center

    # Set the new image surface
    image_rotation = image_rotation.subsurface(rect_rotation).copy()

    return image_rotation

