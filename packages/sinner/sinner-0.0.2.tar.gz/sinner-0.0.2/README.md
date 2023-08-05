## SINNER - Simplest Implementation of Neural Networks for Effortless Runs 

I worked with Neural Networks more years ago than I'd like to remember. I'm returning to study "black box models", and I felt that there is no simple way of creating a neural network, and that was a mistake. That's why I've created this Python library.

Creating a new neural network is (and always will be) as simple as `NeuralNetwork(list)`, where `list` is a list of integers with the number of neurons on every layers (the first one being the input, the last one the output, and the rest the hidden ones). Of course there are and will be optional parameters, but it will always work with a standard view for starters.

Of course "simplest" is not the same as "simplistic", and every aspect of a neural network that makes this implementation more robust is welcome.

---
### Public methods
This list needs to be as short as possible, always. Nowadays we have three methods only:

`eval(inputs)`: eval an array of inputs with current configuration of the neural network.

`train(trainingInputs, trainingOutputs)`: train the network from a set of inputs and outputs

`export(filePath)`: export a JSON representation of the neural network to an external file

You can also create a neural network from a JSON file by calling `NeuralNetwork.fromFile(filePath)`.

---
### Usage

This project is available as a package on [PyPI.org](https://pypi.org/project/sinner/)

---
### To Do List

* add a log system for training outputs
* add usage examples on Git
* make transfer functions selectable on creating
* improve public methods documentation (swagger?)
* add automated tests

---
The original version of this implementation was loosely based on [Jason Brownlee's "How to Code a Neural Network with Backpropagation In Python (from scratch)"](https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/) 

---
Comments and suggestions, feel free to contact me!

--Friar Hob
