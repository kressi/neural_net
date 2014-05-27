"""
train_mnist
~~~~~~~~~~~~~~

"""

#### Libraries
# Standard library
import cPickle
from multiprocessing import Process

# My library
from network import Network
from mnist_loader import load_data_wrapper
from redis_connector import redis


def train_mnist():
    if redis.exists('nn-status'):
        return redis.get('nn-status')
    else:
	Process(target=train_mnist_worker).start()
        return 'Traninig started'

def train_mnist_worker():
    redis.set('nn-status', 'train_mnist: started')
    net = Network([784, 15, 10])
    training_data, validation_data, test_data = load_data_wrapper()
    redis.set('nn-status', 'train_mnist: training with mnist data')
    net.SGD(training_data, 20, 2, 0.1, 0.0001)
    redis.set('nn-weights', cPickle.dumps(net.weights))
    redis.set('nn-biases', cPickle.dumps(net.biases))
    redis.set('nn-status', 'train_mnist: trained')


if __name__ == "__main__":
    train_mnist()
