from PIL import Image
from types import SimpleNamespace
import cherrypy
import imagehash
import json

from colors import compute_top_colors_of_image


def jsonify_error(status, message, traceback, version):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status': status, 'message': message})


class V1(object):
    @staticmethod
    def read_image():
        body = cherrypy.request.body
        return Image.open(body)

    @staticmethod
    def generate_hash(hash_function):
        image = V1.read_image()
        return V1.generate_hash_from_image(hash_function, image)

    @staticmethod
    def generate_hash_from_image(hash_function, image):
        hash_object = hash_function(image)
        return str(hash_object)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def average_hash(self):
        return {'average_hash': V1.generate_hash(imagehash.average_hash)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def difference_hash(self):
        return {'difference_hash': V1.generate_hash(imagehash.dhash)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def perception_hash(self):
        return {'perception_hash': V1.generate_hash(imagehash.phash)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def wavelet_hash(self):
        return {'wavelet_hash': V1.generate_hash(imagehash.whash)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def hashes(self):
        image = V1.read_image()
        average = V1.generate_hash_from_image(imagehash.average_hash, image)
        difference = V1.generate_hash_from_image(imagehash.dhash, image)
        perception = V1.generate_hash_from_image(imagehash.phash, image)
        wavelet = V1.generate_hash_from_image(imagehash.whash, image)
        return {'average_hash': average,
                'difference_hash': difference,
                'perception_hash': perception,
                'wavelet_hash': wavelet}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def colors(self, n):
        image = V1.read_image()
        try:
            n = int(n)
        except ValueError:
            raise cherrypy.HTTPError(400, 'Parameter n must be valid int')
        return compute_top_colors_of_image(image, n)


if __name__ == '__main__':
    root = SimpleNamespace()
    root.v1 = V1()
    cherrypy.quickstart(cherrypy.tree.mount(root, "/"),
                        config='./config/cherrypy.conf')
