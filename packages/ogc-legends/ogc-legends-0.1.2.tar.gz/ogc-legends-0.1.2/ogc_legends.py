import sys
import logging
import requests
from owslib.wms import WebMapService
import os
from collections import defaultdict


__version__ = "0.1.2"
log = logging.getLogger("ogc-legends")


def make_legend_request(url, image_fn):
    """
    Retrieve an image from the url and save it to the output filename
    """
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(image_fn, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
    else:
        log.error("Could not load %s", url)


def get_legends(url, output_folder, regenerate_images=True, version="1.3.0"):
    """
    Get all available legends from a WMS server

    Parameters
    ----------

    url: string
        The URL of the WMS server
    output_folder: string
        The folder to save generated WMS images
    regenerate_images: boolean
        Should images be recreated if they exist on disk already (defaults to True)
    version: string
        The WMS version number - either 1.1.1 or 1.3.0

    Returns
    -------

    dict
        A Python dictionary containing the WMS layer names as keys
        with a list of styles and generated filenames as values

    """

    wms = WebMapService(url, version=version)
    legends = defaultdict(list)

    for layer_name in sorted(wms.contents):
        styles = wms[layer_name].styles
        for style_name, props in styles.items():

            if "legend_format" in props and "/" in props["legend_format"]:
                extension = props["legend_format"].split("/")[1].lower()
            else:
                # default to png - "legend_format" is not in WMS 1.1.1
                extension = "png"

            style_friendly_name = style_name.lower().replace(" ", "_")
            output_fn = "{}_{}.{}".format(layer_name, style_friendly_name, extension)
            print(output_fn)
            image_fn = os.path.join(output_folder, output_fn)

            if regenerate_images is True or not os.path.exists(image_fn):
                url = props["legend"]
                make_legend_request(url, image_fn)

            legends[layer_name].append({"file": image_fn, "style": style_name})

    return legends


if __name__ == "__main__":
    url = sys.argv[1]
    output_folder = sys.argv[2]

    if len(sys.argv) == 4:
        regenerate_images = bool(sys.argv[3])
    else:
        regenerate_images = True

    if len(sys.argv) == 5:
        version = sys.argv[4]
    else:
        version = "1.3.0"

    get_legends(url, output_folder, regenerate_images, version)
