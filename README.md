# neural_net
<a href="https://travis-ci.org/kressi/neural_net"><img src="https://travis-ci.org/kressi/neural_net.svg?branch=master" alt="Build Status" /></a>

http://kressi.github.io/neural_net

## Api
[http://neural-net.herokuapps.com/\<method\>](http://neural-net.herokuapp.com/api)

All the method parameters are sent via POST. Responses are in JSON.

In case the operation could be executed successfully, the response does not always contain a message.
{ "success": 1, ... }

The response will always contain a message in case of an error.
{ "success": 0, "message": "\<error text\>" }


### attributes
all attributes except success are optional.

- success: integer. 0: unsuccessful execution. 1: successful execution
- message: string. contains error message in case of unsuccessful exection.

- net-id: string. containing id of neural-net. default: 'nn'
- epochs: integer. number of epochs the neural net has to be trained for. with other values default one epoche takes around 50s to be trained. default: 30
- mini-batch-size: integer. training sets, after how many patterns the result is back propagated. default: 4
- eta: float. 0 <= eta < 1
- lmbda: float. 0 < lmbda < 1
- pattern: array. resolution of pattern is 28x28 pixels, each pixel is represented by a float value between 0 (white) and 1 (black). the array consists of all the rows appended to each other: [row1, row2, row3 ..., row28], this will result in an array of dimension (1,784).
- result: integer. value between 0 and 9, the number the neural net recognized in the pattern.
- distribution: array. contains the output of the neural net, the number with the highest value is the number recognized as result by the neural net.



### methods

**train-mnist**

net will be created and trained. an already existing net, currently, cannot be trained.

request:
```
{
    "net-id": <string>,
    "epochs": <int>,
    "mini-batch-size": <int>,
    "eta": <float>,
    "lmbda": <float>
}
```

response:
```
{
    "success": <int>,
    "message": <string>
}
```

**delete**

request:
```
{
    "net-id": <string>
}
```

response:
```
{
    "success": <int>,
    "message": <string>
}
```

**recognize**

request:
```
{
    "net-id": <string>,
    "pattern": <array>
}
```

response:
```
{
    "success": <int>,
    "message": <string>,
    "result": <int>,
    "distribution": <array>
}
```

**train** (not implemented yet)

request:
```
{
    "net-id": <string>,
    "pattern": <array>,
    "result": <int>
}
```

response:
```
{
    "success": <int>,
    "message": <string>
}
```

## Documents
- http://neuralnetworksanddeeplearning.com/index.html
- http://yann.lecun.com/exdb/publis/pdf/simard-00.pdf
- http://www.engineering.upm.ro/master-ie/sacpi/mat_did/info068/docum/Neural%20Networks%20for%20Pattern%20Recognition.pdf

## Deployment (Heroku)
https://blog.dbrgn.ch/2013/6/18/heroku-buildpack-numpy-scipy-scikit-learn/

Numpy and Scipy are required for Scikit-learn to run, they cannot simply be installed on Heroku though. Those packages need a Fortran compiler and different libraries for installation, which are not available on Heroku. In order to make them work Heroku requires a custom Python buildpack with Numpy and Scipy included. (https://github.com/kressi/heroku-buildpack-python-sklearn)

On travis the same issue occurs. However, it can be avoided by installing Numpy and Scipy with apt before installation. By enabling system_site_packages in virtualenv travis uses those packages. Scikit-learn is also installed through apt, just because it is much faster than building it with pip.

To use custom buildpacks, the application must be deployed using git. Travis by default deploys with <a href="https://github.com/ddollar/anvil">Anvil</a>, therefore strategy Git must be set.

