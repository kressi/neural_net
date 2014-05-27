"""
train_mnist
~~~~~~~~~~~~~~

"""

#### Libraries
# Standard library
import cPickle
from multiprocessing import Process

# My library
from network import Network, loads
from mnist_loader import load_data_wrapper
from redis_connector import redis, redis_key


def train_mnist():
    if redis.exists(redis_key('status')):
        return redis.get(redis_key('status'))
    else:
	Process(target=train_mnist_worker).start()
        return 'Traninig started'

def train_mnist_worker():
    redis.set(redis_key('status'), 'train_mnist: started')
    net = Network([784, 15, 10])
    training_data, validation_data, test_data = load_data_wrapper()
    redis.set(redis_key('status'), 'train_mnist: training with mnist data')
    net.SGD(training_data, 20, 2, 0.1, 0.0001)
    redis.set(redis_key('data'), net.tostring())
    redis.set(redis_key('status'), 'train_mnist: trained')

def recognize_pattern(data):
    if !redis.exists('status'):
        return 'net not trained'
    elif redis.get(redis_key('status') == 'train_mnist: trained':
        return 'training of net not finished'
    else:
        net = loads(redis.get(redis_key('data')))
        return net.feedforward(data)

if __name__ == "__main__":
    train_mnist()
