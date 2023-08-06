import threading
import requests 
import os
import traceback

from flask import Flask, render_template, Response, request, make_response, current_app, jsonify
import cv2
from decouple import config
from datetime import datetime, timedelta
from functools import update_wrapper

from backend.classes.camera import VideoCamera
from backend.classes.encode_faces import EncodeFace

app = Flask(__name__)

HTTP_HOST = "0.0.0.0"
HTTP_PORT = 5000

camera = None

class WebServer:

    def __init__(self, camera_class):
        global camera
        camera = camera_class


    def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
        """Decorator function that allows crossdomain requests.
            Courtesy of
            https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
        """
        if methods is not None:
            methods = ', '.join(sorted(x.upper() for x in methods))
        # use str instead of basestring if using Python 3.x
        if headers is not None and not isinstance(headers, basestring):
            headers = ', '.join(x.upper() for x in headers)
        # use str instead of basestring if using Python 3.x
        if not isinstance(origin, str):
            origin = ', '.join(origin)
        if isinstance(max_age, timedelta):
            max_age = max_age.total_seconds()

        def get_methods():
            """ Determines which methods are allowed
            """
            if methods is not None:
                return methods

            options_resp = current_app.make_default_options_response()
            return options_resp.headers['allow']

        def decorator(f):
            """The decorator function
            """
            def wrapped_function(*args, **kwargs):
                """Caries out the actual cross domain code
                """
                if automatic_options and request.method == 'OPTIONS':
                    resp = current_app.make_default_options_response()
                else:
                    resp = make_response(f(*args, **kwargs))
                if not attach_to_all and request.method != 'OPTIONS':
                    return resp

                h = resp.headers
                h['Access-Control-Allow-Origin'] = origin
                h['Access-Control-Allow-Methods'] = get_methods()
                h['Access-Control-Max-Age'] = str(max_age)
                h['Access-Control-Allow-Credentials'] = 'true'
                h['Access-Control-Allow-Headers'] = \
                    "Origin, X-Requested-With, Content-Type, Accept, Authorization"
                if headers is not None:
                    h['Access-Control-Allow-Headers'] = headers
                return resp

            f.provide_automatic_options = False
            return update_wrapper(wrapped_function, f)
        return decorator
    

    def startServer(self):
        global HTTP_HOST
        global HTTP_PORT
        print(" [*] Starting WebServer.")
        app.run(host=HTTP_HOST, debug=False, port=HTTP_PORT)

    @app.route('/video_feed', methods=['GET', 'OPTIONS'])
    def video_feed():

        global camera

        def gen(camera_videofeed):
            try:
                while True:
                    frame, _ = camera_videofeed.get_frame()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            except Exception as e:
                print(str(e))
                print(traceback.format_exc())

        return Response(gen(camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/mode/<mode>', methods=['GET', 'OPTIONS'])
    @crossdomain(origin='*')
    def set_mode(mode):
        global camera

        # modes: register and detect

        camera.mode = mode

        return jsonify({"status": True})

    @app.route('/getcod/<cpf>', methods=['GET', 'OPTIONS'])
    @crossdomain(origin='*')
    def get_cpf(cpf):
        result_response = {
            "status": True,
            "message": "Operação realizada com sucesso."
        }

        try:

            data = {
                "CPF": cpf
            }

            r = requests.post(url = 'http://briansilva1.zeedhi.com/workfolder/integracao-catraca/backend/service/index.php/getcodbycpf', data = data)
            result = r.json() 
            if(result['status']):
                result_response['CDFUNC'] = result['CDFUNC']        
            else:
                raise Exception(result['mensagem'])
        
        except Exception as e:
            result_response['status'] = False
            result_response['message'] = str(e)


        return jsonify(result_response)

    


    @app.route('/takepersonphoto/<person_cpf>', methods=['GET', 'OPTIONS'])
    @crossdomain(origin='*')
    def register_person(person_cpf):
        global camera

        result_response = {
            "status": True,
            "message": "Operação realizada com sucesso."
        }

        try:

            if (camera.mode != 'register'):
                raise Exception('Modo de registro não está ativo')

            data = {
                "CPF": person_cpf
            }

            # sending get request and saving the response as response object
            r = requests.post(url = 'http://briansilva1.zeedhi.com/workfolder/integracao-catraca/backend/service/index.php/getcodbycpf', data = data)

            result = r.json()

            if (result['status']):
                    
                person_cod = result['CDFUNC']

                path = './face_recognition/dataset/' + str(person_cod)
                if os.path.exists(path) == False:
                    os.makedirs(path)          
                _, frame = camera.get_frame()
                date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                img_name = "/"+date+".jpg"
                cv2.imwrite(path+img_name,frame)
            
            else:
                raise Exception(result['message'])
        
        except Exception as e:
            result_response['status'] = False
            result_response['message'] = str(e)
            print(str(e))
            print(traceback.format_exc())

        return jsonify(result_response)

    @app.route('/startTraining', methods=['GET', 'OPTIONS'])
    @crossdomain(origin='*')
    def start_training():
        encodeFace = EncodeFace()
        response = encodeFace.enconde()        
        return jsonify(response)



    def main(self):    
        t1 = threading.Thread(target=self.startServer, daemon=True )
        t1.start()