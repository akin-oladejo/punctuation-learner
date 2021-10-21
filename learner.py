import numpy as np

from loader import Loader

# maybe consider removing the sigmoid step from the model
# maybe consider removing the sigmoid step from the model
class Learner:
    def __init__(self, lr=0.1):
        np.random.seed(32) # set seed
        self._lr = lr

    def set_seed(self, val):
        '''
        Set random seed.
        Parameters
        ----------
        val : Int : number to set numpy.random.seed()
        '''
        np.random.seed(val)


    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def mse(self, pred): # loss function
        return np.mean(np.square(pred-self._label)) 

    def weights(self, w=None):
        if w: self._weights = w
        return f'Weights:\n {self._weights}'

    def bias(self, b=None):
        if b: self._bias = b
        return f'Bias:\n {self._bias}'

    def params(self):
        return self.weights() + '\n' + self.bias()

    def model(self, input=None, w=None, b=None):
        if not isinstance(w, np.ndarray): w = self._weights
        if not b: b = self._bias
        if not input: input = self._features
        return self.sigmoid(np.dot(input, w) + b)

    def grad_w(self, loc, delta):
        # calculate gradient of weight
        # loc stands for the index of the weight to calculate gradients for
        weights_plus = self._weights.copy()
        weights_plus[loc] = weights_plus[loc]+delta # create copy of weights where that particular weight is bigger for grad purposes

        weights_minus = self._weights.copy()
        weights_minus[loc] = weights_minus[loc]-delta # create copy of weights where that particular weight is smaller for grad purposes

        change_in_loss = self.mse(self.model(w=weights_plus, b=self._bias)) - \
                         self.mse(self.model(w = weights_minus, b=self._bias))
        change_in_weight = delta*2
        return change_in_loss/change_in_weight # return gradient

    def grad_b(self, delta):
        # calculate gradient of bias
        change_in_loss = self.mse(self.model(w=self._weights, b=self._bias+delta)) - \
               self.mse(self.model(w=self._weights, b=self._bias-delta))
        change_in_bias = delta*2
        return change_in_loss/change_in_bias # return gradient

    def backwards(self, delta=0.1):
        lr = self._lr

        #update weight
        for i in range(len(self._weights)):
            self._weights[i] -= lr*self.grad_w(loc=i, delta=delta)

        # update bias
        self._bias -= lr*self.grad_b(delta=delta)

    def plot_loss(self, x, y, x_label, y_label, title):
        plt.scatter(x,y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    def train(self, features, label, epochs=150, plot=False):
        self._weights = np.random.rand(features.shape[-1], 1) # initialize weights
        self._bias = np.random.rand(1) # initialize bias
        self._loss = [] # track loss
        self._epoch = [] # track epoch
        self._features = features # store input
        self._label = label # store output
        print(f'Parameters before fitting:\n{self.params()}\n-------')
        for i in range(epochs):
            preds = self.model()
            loss = self.mse(preds)
            self.backwards()
            self._epoch.append(i) # add to epoch counter
            self._loss.append(self.mse(preds))
        if plot == True: self.plot_loss(self._epoch, self._loss, 'epoch', 'loss', 'Training Progress')
        print(f'\n-------\nParameters after fitting:\n{self.params()}')

    def predict(self, input): 
        return 1 if self.model(input).item() > 0.5 else 0