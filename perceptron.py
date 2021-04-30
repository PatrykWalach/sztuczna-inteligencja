
import random
import math


def default_activator(n: float):
    if n >= 1:
        return 1
    return 0


def sigmoid(n: float):
    return 1 / (1+math.exp(-n))


class Perceptron:
    def __init__(self, inputs: int, **kwargs):
        weights = kwargs.get('weights', [])
        rand = kwargs.get('random', lambda: random.uniform(-2.0, 2.0))
        activator = kwargs.get('activator', sigmoid)

        if(inputs < 1):
            raise ValueError('inputs less than one.')

        if(len(weights) > inputs):
            raise ValueError('Bad weights length.')

        self.inputs = inputs
        self.activator = activator
        self.weights = [
            weights[i] if i < len(weights) and weights[i] is not None else rand() for i in range(inputs)]

    def guess(self, inputs: list):
        if(len(inputs) != self.inputs):
            raise ValueError('Bad inputs length.')

        return self.activator(sum(i*w for i, w in zip(inputs, self.weights)))

    def train(self, inputs: list, target):
        if(len(inputs) != self.inputs):
            raise ValueError('Bad inputs length.')

        guess = self.guess(inputs)
        error = target-guess
        self.weights = [w+0.1*error*i for w, i in zip(self.weights, inputs)]


class NeuralNetwork:
    def __init__(self, inputs: int,  outputs: int, **kwargs):
        rand = kwargs.get('random', lambda: random.uniform(-2.0, 2.0))
        activator = kwargs.get('activator', sigmoid)

        if(inputs < 1):
            raise ValueError('inputs less than one.')

        self.inputs = inputs
        self.outputs = outputs
        self.perceptrons = [Perceptron(
            inputs+1, activator=activator, random=rand) for i in range(outputs)]

    def guess(self, inputs: list):
        if(len(inputs) != self.inputs):
            raise ValueError('Bad inputs length.')

        return [p.guess(inputs+[1]) for p in self.perceptrons]

    def train(self, inputs: list, targets: list):
        if(len(inputs) != self.inputs):
            raise ValueError('Bad inputs length.')

        if(len(targets) != self.outputs):
            raise ValueError('Bad targets length.')

        guesses = self.guess(inputs)

        for p, target in zip(self.perceptrons, targets):
            p.train(inputs+[1], target)


def split_seq(seq, **kwargs):
    arr = list(seq)
    index = kwargs.get('index', len(arr)//2)
    return arr[:index], arr[index:]


if __name__ == '__main__':
    with open('funkcje-logiczne.csv') as f:
        data = f.read()

    n = NeuralNetwork(inputs=3, outputs=3, activator=default_activator)

    for i in range(50):
        for inputs, outputs in [split_seq(map(float, l.split(',')), index=3) for l in data.split('\n')[1:]]:
            n.train(inputs, outputs)

    print(n.guess([0, 0, 0]))
    print(n.guess([0, 0, 1]))
    print(n.guess([0, 1, 0]))
    print(n.guess([0, 1, 1]))
    print(n.guess([1, 0, 0]))
    print(n.guess([1, 0, 1]))
    print(n.guess([1, 1, 0]))
    print(n.guess([1, 1, 1]))
