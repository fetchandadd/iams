from PIL import Image
from types import SimpleNamespace
import cherrypy
import imagehash


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


if __name__ == '__main__':
    root = SimpleNamespace()
    root.v1 = V1()
    cherrypy.quickstart(cherrypy.tree.mount(root, "/"),
                        config='./cherrypy.conf')
