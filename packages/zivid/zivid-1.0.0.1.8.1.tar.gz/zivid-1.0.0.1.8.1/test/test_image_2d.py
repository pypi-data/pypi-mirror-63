import pytest


@pytest.mark.physical_camera
def test_to_array(physical_camera_image_2d):
    import numpy

    raw_image = physical_camera_image_2d.to_array()
    assert raw_image is not None
    assert isinstance(raw_image, numpy.ndarray)


@pytest.mark.physical_camera
def test_save_path(physical_camera_image_2d):
    from pathlib import Path

    physical_camera_image_2d.save(Path("some_file.png"))


@pytest.mark.physical_camera
def test_save_string(physical_camera_image_2d):
    physical_camera_image_2d.save("some_file.png")


@pytest.mark.physical_camera
def test_to_array_context_manager(physical_camera_frame_2d):
    with physical_camera_frame_2d.image() as image_2d:
        image_2d.to_array()
    with pytest.raises(RuntimeError):
        image_2d.to_array()


@pytest.mark.physical_camera
def test_height(physical_camera_image_2d):
    height = physical_camera_image_2d.height

    assert height == 1200
    assert isinstance(height, int)


@pytest.mark.physical_camera
def test_width(physical_camera_image_2d):
    width = physical_camera_image_2d.width

    assert width == 1920
    assert isinstance(width, int)


@pytest.mark.physical_camera
def test_width_context_manager(physical_camera_frame_2d):
    with physical_camera_frame_2d.image() as image_2d:
        image_2d.width  # pylint: disable=pointless-statement
    with pytest.raises(RuntimeError):
        image_2d.width  # pylint: disable=pointless-statement


@pytest.mark.physical_camera
def test_height_context_manager(physical_camera_frame_2d):
    with physical_camera_frame_2d.image() as image_2d:
        image_2d.height  # pylint: disable=pointless-statement
    with pytest.raises(RuntimeError):
        image_2d.height  # pylint: disable=pointless-statement


@pytest.mark.physical_camera
def test_save_context_manager(physical_camera_frame_2d):
    with physical_camera_frame_2d.image() as image_2d:
        image_2d.save("some_file.png")
    with pytest.raises(RuntimeError):
        image_2d.save("some_file.png")
