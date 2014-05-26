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
Numpy and Scipy are required for Scikit-learn to run, they cannot simply be installed on Heroku though. Those packages need a Fortran compiler and different libraries for installation, which are not available on Heroku. In order to make them work Heroku requires a custom Python buildpack with Numpy and Scipy included.
https://github.com/kressi/heroku-buildpack-python-sklearn

To use custom buildpacks, the application must be deployed using git. Travis by default deploys with <a href="https://github.com/ddollar/anvil">Anvil</a>, therefore strategy Git must be set.
