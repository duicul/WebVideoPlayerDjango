from waitress import serve

from WebVideoPlayer.wsgi import application
import cherrypy

if __name__ == '__main__':
    config = {'/static/js':
    {
        'tools.staticfile.on': True,
        'tools.staticfile.dir': "D:\WebAppVideoPlayer\WebVideoPlayer\static\js",
    }
    }
    cherrypy.tree.mount(Root(), config=config)
    serve(application, port='8000')
