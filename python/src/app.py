from PIL import Image
from types import SimpleNamespace
import cherrypy
import imagehash


class V1(object):
    @staticmethod
    def generate_hash(hash_function):
        body = cherrypy.request.body
        image = Image.open(body)
        hash_object = hash_function(image)
        return str(hash_object)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def average_hash(self):
        return {'average_hash': V1.generate_hash(imagehash.average_hash)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def perception_hash(self):
        return {'perception_hash': V1.generate_hash(imagehash.phash)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def difference_hash(self):
        return {'difference_hash': V1.generate_hash(imagehash.dhash)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def wavelet_hash(self):
        return {'wavelet_hash': V1.generate_hash(imagehash.whash)}


if __name__ == '__main__':
    root = SimpleNamespace()
    root.v1 = V1()
    cherrypy.quickstart(cherrypy.tree.mount(root, "/"),
                        config='./cherrypy.conf')
