import io
import os
import urllib
from tornado.options import define
from PIL import Image
import tornado.escape
import tornado.ioloop
import tornado.web
import json
from tornado.escape import json_decode
from models.mtcnn import MTCNN
from models.inception_resnet_v1 import InceptionResnetV1
from FaceRecognition import cosSimilarity, getVec
from utils import getConnection

define("port", default=8080, help="run on the given port", type=int)
tornado.options.parse_command_line()

BASE_DIR = os.path.dirname(__file__)

# FaceNet
mtcnn = MTCNN(image_size=160, margin=10)
resnet = InceptionResnetV1().eval()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        self.render("index.html")


class FaceRecognitionHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        data1 = self.request.files['img_file'][0]['body']
        data2 = self.request.files['img_file'][1]['body']
        img1 = Image.open(io.BytesIO(data1))
        img2 = Image.open(io.BytesIO(data2))

        vec1 = getVec(img1, mtcnn, resnet)
        vec2 = getVec(img2, mtcnn, resnet)
        sim = cosSimilarity(vec1, vec2)
        if sim is not None:
            self.write(json.dumps(str(sim)))

class RegistrationHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):

        req = json_decode(self.request.body)
        img_path = req["image_path"]
        user_id = req["user_id"]
        img = io.BytesIO(urllib.request.urlopen(img_path).read())
        img = Image.open(img).convert('RGB')
        try:
            vector = getVec(img, mtcnn, resnet)
        except:
            self.write(json.dumps({"result" : "-1"}))
            return
        try:
            with getConnection() as conn:
                conn.execute('INSERT INTO userlist (user_id, face_vec) VALUES (%s, %s)', (user_id, list(vector.astype(float))))
            data = {"result" : "1"}
        except: 
            data = {"result" : "0"}
        self.write(json.dumps(data))
        
class GetSimilarFaceHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        req = json_decode(self.request.body)
        user_id = req["user_id"]
        try:
            with getConnection() as conn:
                data = conn.execute('SELECT face_vec FROM userlist WHERE user_id=%s',(user_id,))
                vec_mine = data.fetchone()
                data = conn.execute('SELECT user_id, face_vec FROM userlist WHERE user_id!=%s',(user_id,))
                user_list = data.fetchall()

            sim_list = []
            for user in user_list:
                sim = cosSimilarity(vec_mine[0], user[1])
                if sim > 0.4:
                    sim_list.append([sim, user[0]])

            new_sim_list = sorted(sim_list, reverse=True)
            data = {"user_id": user_id, "list": [x[1] for x in new_sim_list]}
        except:
            data = {"result" : "0"}
        self.write(json.dumps(data))

def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/debug", FaceRecognitionHandler),
            (r"/regist", RegistrationHandler),
            (r"/simlist", GetSimilarFaceHandler)
        ],
        template_path=os.path.join(BASE_DIR, 'templates'),
        static_path=os.path.join(BASE_DIR, 'static'),
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()