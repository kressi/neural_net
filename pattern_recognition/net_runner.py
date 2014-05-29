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


def train_mnist(net_id='nn', params={}):
    if redis.exists(redis_key('status', net_id)):
        return {'success': 0, 'message': redis.get(redis_key('status', net_id))}
    else:
	Process(target=train_mnist_worker, args=(net_id, params)).start()
        return {'success': 1}

def train_mnist_worker(net_id, params):
    net_id = params.get('net-id', 'nn')
    net_params                    = {}
    net_params['net_id']          = net_id
    net_params['epochs']          = params.get('epochs', 1)
    net_params['mini_batch_size'] = params.get('mini-batch-size', 4)
    net_params['eta']             = params.get('eta', 0.1)
    net_params['lmbda']           = params.get('lmbda', 0.0001)

    redis.set(redis_key('params', net_id), json.dumps(net_params))
    redis.set(redis_key('status', net_id), 'train_mnist: started')

    net = Network([784, 15, 10])
    training_data, validation_data, test_data = load_data_wrapper()
    redis.set(redis_key('status', net_id), 'train_mnist: training with mnist data')
    net.SGD(training_data, 30, 2, 0.1, 0.0001)

    redis.set(redis_key('data', net_id), net.tostring())
    redis.set(redis_key('status', net_id), 'train_mnist: trained')

def recognize_pattern(pattern, net_id='nn'):
    redis.keys()
    if not redis.exists(redis_key('status', net_id)):
        return 'net not trained'
    elif redis.get(redis_key('status', net_id)) != 'train_mnist: trained':
        return 'training of net not finished'
    else:
        net = loads(redis.get(redis_key('data', net_id)))
        data = np.zeros((784,1),dtype=float)
        for i, v in enumerate(pattern):
            if v != 0:
                data[i][0] = float(v)
        distribution = net.feedforward(data)
        number = np.argmax(distribution)
        return {'success': 1, 'result': number, 'distribution': distribution }

if __name__ == "__main__":
    train_mnist()
