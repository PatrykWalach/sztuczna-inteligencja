
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
        activator = kwargs.get('activator', default_activator)

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




if __name__ =='__main__':
    with open('xor.csv') as f:
        data = f.read()

    n = Perceptron(inputs=2, weights=[0.3, 0.2])


    for i in range(10):
        for inputs, d in [([float(n) for n in l.split(',')[:-1]], float(l.split(',').pop())) for l in data.split('\n')[1:]]:
            n.train(inputs, d)


    print(n.guess([0, 0]))
    print(n.guess([0, 1]))
    print(n.guess([1, 0]))
    print(n.guess([1, 1]))
