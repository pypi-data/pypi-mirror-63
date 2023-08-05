"""This file imports used classes, modules and packages."""
try:
    from _zivid._zivid import (  # pylint: disable=import-error,no-name-in-module
        __version__,
        Application,
        Camera,
        CameraState,
        environment,
        firmware,
        hand_eye,
        capture_assistant,
        Frame,
        FrameInfo,
        hdr,
        PointCloud,
        Settings,
        version,
        Settings2D,
        Frame2D,
        Image,
    )
except ImportError as ex:
    import platform

    def __missing_sdk_error_message():
        error_message = """Failed to import the Zivid Python C-module, please verify that:
 - Zivid SDK is installed
 - Zivid SDK version is matching the SDK version part of the Zivid Python version """
        if platform.system() != "Windows":
            return error_message
        return (
            error_message
            + """
 - Zivid SDK libraries location is in system PATH"""
        )

    raise ImportError(__missing_sdk_error_message()) from ex
