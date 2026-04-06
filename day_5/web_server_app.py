import cherrypy

#config
cherrypy.config.update({
    "server.socket_host": "0.0.0.0",
    "server.socket_port": 8080,
})


class HelloWorld(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Hello World!"}

cherrypy.quickstart(HelloWorld())