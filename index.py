import os
import sys

ROOT_PATCH = os.path.dirname(os.path.realpath(__file__))
print(ROOT_PATCH)

os.environ.update({'ROOT_PATH':ROOT_PATCH})
os.environ.update({'ENV':'desarrollo'})
os.environ.update({'PUERTO':'4000'})
sys.path.append(os.path.join(ROOT_PATCH, 'modulos'))

from modulos.app import app, mongo

if __name__ == '__main__':
    
    app.config['DEBUG'] = os.environ.get('ENV') == 'desarrollo'
app.run(host = '0.0.0.0', port = int(os.environ.get("PUERTO")))    

