neural_net
==========
<a href="https://travis-ci.org/kressi/neural_net"><img src="https://travis-ci.org/kressi/neural_net.svg?branch=master" alt="Build Status" /></a>

http://kressi.github.io/neural_net

Api
---
http://neural-net.herokuapp.com/api

Documents
---------
- http://neuralnetworksanddeeplearning.com/index.html
- http://yann.lecun.com/exdb/publis/pdf/simard-00.pdf
- http://www.engineering.upm.ro/master-ie/sacpi/mat_did/info068/docum/Neural%20Networks%20for%20Pattern%20Recognition.pdf

Heroku
------
https://blog.dbrgn.ch/2013/6/18/heroku-buildpack-numpy-scipy-scikit-learn/

Numpy and Scipy are required for Scikit-learn to run, they cannot simply be installed on Heroku though. Those packages need a Fortran compiler and different libraries for installation, which are not available on Heroku. In order to make them work Heroku requires a custom Python buildpack with Numpy and Scipy included. (https://github.com/kressi/heroku-buildpack-python-sklearn)

On travis the same issue occurs. However, it can be avoided by installing Numpy and Scipy with apt before installation. Scikit-learn is also installed with apt, just because it is much faster than building it with pip.

To use custom buildpacks, the application must be deployed using git. Travis by default deploys with <a href="https://github.com/ddollar/anvil">Anvil</a>, therefore strategy Git must be set.
