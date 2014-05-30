"""
net_runner.py
~~~~~~~~~~~~~~
Manages networks on Redis and loads stored networks
to recognize patterns.

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

#### Train a new neural net
def train_mnist(params={}):
    """In case network has not been trained a worker
    process will be started and success is returned.
    Success in that situation does not mean the net could
    be trained successfully, this currently cannot be checked.
    The net has finished training as soon as the <net-id>-data
    entry has been made and it shows up in list-nets.
    :params['net-id']: default 'nn'
    :params['epochs']: default 1
    :params['mini-batch-size']: default 4
    :params['lmbda']: 0.0001
    :params['eta']: 0.1
    :params['layers']: [15]
    """
    clean_params(params)
    if 'net-id' not in params.keys():
        params['net-id']='nn'
    r_key = redis_key('status', params['net-id'])
    if redis.exists(r_key):
        return {'success': 0, 'message': redis.get(r_key)}
    else:
	Process(target=train_mnist_worker, args=(params,)).start()
        return {'success': 1}

def train_mnist_worker(params):
    net_id = params.get('net-id', 'nn')
    layers = [784]
    layers.extend([int(i) for i in params.get('layers', [15])])
    layers.append(10)
    net_params                    = {}
    net_params['epochs']          = int(params.get('epochs', 1))
    net_params['mini_batch_size'] = int(params.get('mini-batch-size', 4))
    net_params['eta']             = float(params.get('eta', 0.1))
    net_params['lmbda']           = float(params.get('lmbda', 0.0001))
    net_params['layers']          = layers

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

#### List trained nets
def list_nets():
    """Returns a list of all trained nets and the parameters
    they were created with.
    """
    nets = filter(lambda x: x.split('-')[-1] == 'data', redis.keys())
    if nets.__len__() > 0:
        net_ids = (x[:x.rfind('-')] for x in nets)
        nets = dict((key, json.loads(redis.get(redis_key('params', key)))) for key in net_ids)
        return nets

#### Delete all to net-id related redis entries
def delete_net(net_id):
    if net_id[:2] == 'nn':
      return {'success': 0, 'messag': 'nn cannot be deleted'}
    count=0
    for key in redis.keys():
        if key[:key.rfind('-')] == net_id:
            count += redis.delete(key)
    sccs = 1 if count > 0 else 0
    return {'success': sccs, 'message': '%d records from net %s deleted' % (count, net_id)}

#### Recognize pattern
def recognize_pattern(params):
    clean_params(params)
    net_id = params.get('net-id', 'nn')
    pattern = params.get('pattern')
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

#### Helper Functions
def clean_params(params):
    """Delete empty strings and None entries from dict
    """
    for key, value in params.items():
        if value in [None, ""]:
            del params[key]
