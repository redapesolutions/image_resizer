import flask
from PIL import Image
import os
app = flask.Flask(__name__)

ORIGINAL_FOLDER = '/home/azureuser/original'
ASSETS_FOLDER = '/home/azureuser/assets'

def abort_if_no_path(path):
    if not path:
        flask.abort(404)

class InvalidSize(Exception):
    pass


def clean_size_parameters(w, h):
    if w == 'x':
        w = None
    else:
        try:
            w = int(w)
        except:
            raise InvalidSize
    if h == 'x':
        h = None
    else:
        try:
            h = int(h)
        except:
            raise InvalidSize

    if h is None and w is None:
        raise InvalidSize 

    return (w, h)


def resize_image(im, width, height):
    if width is None or height is None:
        # We need to read the size
        original_width, original_height = im.size

        if width is None:
            ratio = float(height) / float(original_height)
            width = int(original_width * ratio)

        else:
            ratio = float(width) / float(original_width)
            height = int(original_height * ratio)
    
    size = (width, height)

    return im.resize(size, Image.ANTIALIAS)

@app.route('/<path:image_path>', methods=['GET'])
def index(image_path):
    # Parse file - width and height should be in the last two "subfolders"
    path, s, filename = image_path.rpartition('/')
    # Make sure we have a path left after cutting off

    abort_if_no_path(path)
    # get the last 2
    path, s, height = path.rpartition('/')
    abort_if_no_path(path)
    path, s, width = path.rpartition('/')

    # get options depending on height and width found
    try:
        width, height = clean_size_parameters(width, height)
    except InvalidSize:
        flask.abort(500)

    # Try loading the original image
    # original does not include width and height
    original = '{}/{}/{}'.format(ORIGINAL_FOLDER, path, filename)
    destination = '{}/{}'.format(ASSETS_FOLDER, image_path)

    try:
        im = Image.open(original)
    except IOError:
        flask.abort(404)
    resized = resize_image(im, width, height)
    print resized, destination
    folder = os.path.dirname(destination)
    try:
        os.makedirs(folder)
        resized.save(destination)
    except OSError:
        # This means folder already exists
        pass

    try:
        return flask.send_from_directory(folder, filename)
    except Exception as e:
        print e


