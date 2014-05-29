"""
train_mnist
~~~~~~~~~~~~~~

"""

#### Libraries
# Standard library
import cPickle
import numpy as np
import json
from multiprocessing import Process

# My library
from network import Network, loads
from mnist_loader import load_data_wrapper
from redis_connector import redis, redis_key


def train_mnist(params={}):
    if 'net-id' not in params.keys():
        params['net-id']='nn'
    if redis.exists(redis_key('status', params['net-id'])):
        return {'success': 0, 'message': redis.get(redis_key('status', net_id))}
    else:
	Process(target=train_mnist_worker, args=(params,)).start()
        return {'success': 1}

def train_mnist_worker(params):
    net_id = params.get('net-id', 'nn')
    layers = [784]
    layers.extend(params.get('layers', [15]))
    layers.append(10)
    net_params                    = {}
    net_params['epochs']          = params.get('epochs', 1)
    net_params['mini_batch_size'] = params.get('mini-batch-size', 4)
    net_params['eta']             = params.get('eta', 0.1)
    net_params['lmbda']           = params.get('lmbda', 0.0001)
    net_params['layers']          = layers

    print json.dumps(net_params)

    redis.set(redis_key('params', net_id), json.dumps(net_params))
    redis.set(redis_key('status', net_id), 'train_mnist: started')

    net = Network(layers)
    training_data, validation_data, test_data = load_data_wrapper()
    redis.set(redis_key('status', net_id), 'train_mnist: training with mnist data')
    net.SGD(training_data, net_params['epochs'],
                           net_params['mini_batch_size'],
                           net_params['eta'],
                           net_params['lmbda'])

    redis.set(redis_key('data', net_id), net.tostring())
    redis.set(redis_key('status', net_id), 'train_mnist: trained')

def recognize_pattern(pattern, net_id='nn'):
    redis.keys()
    status = redis.get(redis_key('status', net_id))
    if status == None:
        return {'success': 0, 'message': 'net not trained'}
    elif status != 'train_mnist: trained':
        return {'success': 0, 'message': status}
    else:
        net = loads(redis.get(redis_key('data', net_id)))
        data = np.zeros((784,1),dtype=float)
        for i, v in enumerate(pattern):
            if v != 0:
                data[i][0] = float(v)
        distribution = list(x[0] for x in net.feedforward(data))
        number = np.argmax(distribution)
        return {'success': 1, 'result': number, 'distribution': distribution }

if __name__ == "__main__":
    train_mnist()
