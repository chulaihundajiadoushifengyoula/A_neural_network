import unittest
from Ann import Ann, timeit
import numpy as np
import random
import copy
import os
import pickle
import logging

logger = logging.getLogger(__name__)

class Test(unittest.TestCase):

    def init_logger(self, level='info'):
        if (level == 'debug'):
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
    
    def setUp(self):
        self.init_logger('debug')

    @timeit
    def test_1(self):
        # Test for Ann Architecture#
        
        # First architecture test#
        n_i1 = 4  # Number of input neurons
        n_h1 = 2  # Number of hidden layers
        n_o1 = 1  # Number of output neurons
        
        ann1 = Ann(n_i=4, n_h=2 , n_o=1)  # Create this architecture
        self.assertEqual(n_i1, ann1.n_i)
        self.assertEqual(n_h1, ann1.n_h)
        self.assertEqual(n_o1, ann1.n_o)
        
        self.assertEqual(ann1.s, [5, 5, 5, 2])
        self.assertEqual(len(ann1.Thetas), 3)
        self.assertEqual(ann1.Thetas[0].shape, (4, 5))
        self.assertEqual(ann1.Thetas[1].shape, (4, 5))
        self.assertEqual(ann1.Thetas[2].shape, (1, 5))
        
        # Second architecture test#
        n_i2 = 10  # Number of input neurons
        n_h2 = 1  # Number of hidden layers
        n_o2 = 2  # Number of output neurons
        
        ann2 = Ann(n_i=n_i2, n_h=n_h2, n_o=n_o2)  # Create this architecture
        self.assertEqual(n_i2, ann2.n_i)
        self.assertEqual(n_h2, ann2.n_h)
        self.assertEqual(n_o2, ann2.n_o)
        
        self.assertEqual(ann2.s, [11, 11, 3])
        self.assertEqual(len(ann2.Thetas), 2)
        self.assertEqual(ann2.Thetas[0].shape, (10, 11))
        self.assertEqual(ann2.Thetas[1].shape, (2, 11))
        
        # Third architecture test#
        n_i3 = 100  # Number of input neurons
        n_h3 = 0  # Number of hidden layers
        n_o3 = 10  # Number of output neurons
        
        ann3 = Ann(n_i=n_i3, n_h=n_h3, n_o=n_o3)  # Create this architecture
        self.assertEqual(n_i3, ann3.n_i)
        self.assertEqual(n_h3, ann3.n_h)
        self.assertEqual(n_o3, ann3.n_o)
        
        self.assertEqual(ann3.s, [101, 11])
        self.assertEqual(len(ann3.Thetas), 1)
        self.assertEqual(ann3.Thetas[0].shape, (10, 101))
        
        n_i4 = 1500  # Number of input neurons
        n_h4 = 3  # Number of hidden layers
        n_o4 = 6  # Number of output neurons
        
        # Fourth architecture test#
        ann4 = Ann(n_i=n_i4, n_h=n_h4, n_o=n_o4)  # Create this architecture
        self.assertEqual(n_i4, ann4.n_i)
        self.assertEqual(n_h4, ann4.n_h)
        self.assertEqual(n_o4, ann4.n_o)
        
        self.assertEqual(ann4.s, [1501, 31 + 1, 31 + 1, 31 + 1, 6 + 1])
        self.assertEqual(len(ann4.Thetas), 4)
        self.assertEqual(ann4.Thetas[0].shape, (31, 1501))
        self.assertEqual(ann4.Thetas[1].shape, (31, 32))
        self.assertEqual(ann4.Thetas[2].shape, (31, 32))
        self.assertEqual(ann4.Thetas[3].shape, (6, 32))
        
        # Fourth (arbitrary) architecture test#
        s = [3, 2]
        n_i = 4
        n_h = len(s)
        n_o = 2
        ann1 = Ann(s=s, n_i=n_i, n_h=n_h, n_o=n_o)  # Create this architecture
        self.assertEqual(n_i, ann1.n_i)
        self.assertEqual(n_h, ann1.n_h)
        self.assertEqual(n_o, ann1.n_o)
        
        self.assertEqual(ann1.s, [5, 3, 2, 3])
        self.assertEqual(len(ann1.Thetas), 3)
        self.assertEqual(ann1.Thetas[0].shape, (2, 5))
        self.assertEqual(ann1.Thetas[1].shape, (1, 3))
        self.assertEqual(ann1.Thetas[2].shape, (2, 2))

    @timeit
    def test_2(self):
        # Test for forward-propagation#
         
        # First architecture test#
        # Logistic regression (0 hidden layers) forward propagation test#
        n_i1 = 4  # Number of input neurons
        n_h1 = 0  # Number of hidden layers
        n_o1 = 1  # Number of output neurons
         
        ann1 = Ann(n_i=n_i1, n_h=n_h1, n_o=n_o1)  # Create this architecture
        x1 = [1, 2, 3, 4]  # Array as first example
        x2 = [-1, -1, -1, -1]  # Array as second example
         
        # Set all weights to zero#
        for i in range(0, len(ann1.Thetas)):
            shape = ann1.Thetas[i].shape
            self.assertEqual(shape, (1, 5))
            ann1.Thetas[i] = np.zeros(shape)
        self.assertEqual(ann1.h(x1), 0.5)
        self.assertEqual(ann1.h(x2), 0.5)
         
        # Set all weights to one#
        for i in range(0, len(ann1.Thetas)):
            shape = ann1.Thetas[i].shape
            self.assertEqual(shape, (1, 5))
            ann1.Thetas[i] = np.ones(shape)
        self.assertAlmostEqual(ann1.h(x1), 0.999, delta=0.001)
        self.assertAlmostEqual(ann1.h(x2), 0.0474, delta=0.0001)
         
        # Set all weights randomly between -1 and 1 (and test the range of output)#
        ann1 = Ann(n_i=n_i1, n_h=n_h1, n_o=n_o1)  # Create this architecture
        self.assertAlmostEqual(ann1.h(x1), 0.5, delta=0.5)  # Sigmoid always gives values between 0 and 1
        self.assertAlmostEqual(ann1.h(x2), 0.5, delta=0.5)
         
        # Custom Thetas weights#
        M = np.matrix([[1, -1, 0.5, -0.3, 2]])
        ann1.Thetas[0] = M
        self.assertAlmostEqual(ann1.h(x1), 0.786, delta=0.001)
        self.assertAlmostEqual(ann1.h(x2), 0.858, delta=0.001)
         
        # Second architecture test#
        # 1 hidden layer forward propagation test#
        n_i1 = 4  # Number of input neurons
        n_h1 = 1  # Number of hidden layers
        n_o1 = 1  # Number of output neurons
         
        ann1 = Ann(n_i=n_i1, n_h=n_h1, n_o=n_o1)  # Create this architecture
        x1 = [1, 2, 3, 4]  # Array as first example
        x2 = [-1, -1, -1, -1]  # Array as second example
         
        # Set all weights to zero#
        for i in range(0, len(ann1.Thetas)):
            shape = ann1.Thetas[i].shape
            ann1.Thetas[i] = np.zeros(shape)
        self.assertEqual(ann1.h(x1), 0.5)
        self.assertEqual(ann1.h(x2), 0.5)
         
        # Set all weights to one#
        for i in range(0, len(ann1.Thetas)):
            shape = ann1.Thetas[i].shape
            ann1.Thetas[i] = np.ones(shape)
        self.assertAlmostEqual(ann1.h(x1), 0.993, delta=0.001)
        self.assertAlmostEqual(ann1.h(x2), 0.767, delta=0.001)  
         
        # Set all weights randomly between -1 and 1 (and test the range of output)#
        ann1 = Ann(n_i=n_i1, n_h=n_h1, n_o=n_o1)  # Create this architecture
        self.assertAlmostEqual(ann1.h(x1), 0.5, delta=0.5)  # Sigmoid always gives values between 0 and 1
        self.assertAlmostEqual(ann1.h(x2), 0.5, delta=0.5)
         
        # Custom Thetas weights#
        M1 = np.matrix([[1, -1, 0.5, -0.3, 2],
                       [1, -1, 0.5, -0.3, 2],
                       [1, -1, 0.5, -0.3, 2],
                       [1, -1, 0.5, -0.3, 2]])
        M2 = np.matrix([[1, 1, -1, 0.5, -1]])
        ann1.Thetas[0] = M1
        ann1.Thetas[1] = M2
        # a^(1) Should be [0.786 0.786 0.786 0.786 1]^T#
        self.assertAlmostEqual(ann1.h(x1), 0.545, delta=0.001)
        # a^(1) Should be [0.858 0.858 0.858 0.858 1]^T#
        self.assertAlmostEqual(ann1.h(x2), 0.571, delta=0.001)
         
    @timeit
    def test_3(self):
         
        # Test the dimensions of the Jacobian matrices against Theta matrices for first architecture#
        n_i1 = 4  # Number of input neurons
        n_h1 = 2  # Number of hidden layers
        n_o1 = 2  # Number of output neurons
         
        ann1 = Ann(n_i=n_i1, n_h=n_h1, n_o=n_o1)  # Create this architecture
        x1 = [1, 2, 3, 4]  # Array as first example
        y1 = [1, 0]
        J = ann1.backward(x1, y1)
        for l in range(0, ann1.L - 1):
            self.assertEqual(ann1.Thetas[l].shape, J[l].shape)
             
        # Test the dimensions of the Jacobian matrices against Theta matrices for second architecture#
        n_i1 = 40  # Number of input neurons
        n_h1 = 3  # Number of hidden layers
        n_o1 = 10  # Number of output neurons
         
        ann1 = Ann(n_i=n_i1, n_h=n_h1, n_o=n_o1)  # Create this architecture
        x1 = 10 * [1, 2, 3, 4]  # Array as first example
        y1 = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
        J = ann1.backward(x1, y1)
        for l in range(0, ann1.L - 1):
            self.assertEqual(ann1.Thetas[l].shape, J[l].shape)
             
        # Test the dimensions of the Jacobian matrices against Theta matrices for third architecture#
        n_i1 = 40  # Number of input neurons
        n_h1 = 0  # Number of hidden layers
        n_o1 = 10  # Number of output neurons
         
        ann1 = Ann(n_i=n_i1, n_h=n_h1, n_o=n_o1)  # Create this architecture
        x1 = 10 * [1, 2, 3, 4]  # Array as first example
        y1 = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
        J = ann1.backward(x1, y1)
        for l in range(0, ann1.L - 1):
            self.assertEqual(ann1.Thetas[l].shape, J[l].shape)
             
    @timeit
    def test_4(self):
        # Gradient checking (check that a numerical approximation of the gradient is (almost) equal to our backpropagation derivation)#
         
        # First data-set with one example
        arrs = []
        labels = []
        arrs.append([1, 2, 4, 5, 5, 5])
        labels.append('cat')
        ann = Ann(arrs, labels, n_h=10)  # Create Ann with these train_examples and labels
        J = ann.backward(ann.train_examples[0].arr, ann.train_examples[0].y)
        T_original = copy.deepcopy(ann.Thetas)
         
        for l in range(0, ann.L - 1):
            shape_J = J[l].shape
            eps = 0.0001  # epsilon for a numerical approximation of the gradient
            for i in range(0, shape_J[0]):
                for j in range(0, shape_J[1]):
                    T_e = np.zeros(shape_J)  # Matrix of zeros
                    T_e[i][j] = eps
                    ann.Thetas[l] = T_original[l] + T_e
                    cost_e = ann.cost()  # Cost at Theta + eps
                    ann.Thetas[l] = T_original[l] - T_e
                    cost_minus_e = ann.cost()  # Cost at Theta - eps
                    P = (cost_e - cost_minus_e) / (2 * eps)  # Numerical approximation
                    J_ij = J[l].item(i, j)  # Backpropagation derivation
                     
                    # print(P, '\t', J_ij, '\t', abs(P - J_ij), (l, i, j))
                     
                    # if (P < 0 and J_ij > 0 or P > 0 and J_ij < 0):
                    #    self.fail()
                     
                    self.assertAlmostEqual(P, J_ij, delta=0.001)
                    ann.Thetas = copy.deepcopy(T_original)
         
        # Second data-set with several train_examples
        arrs = []
        labels = []
        classes = ('cat', 'dog')
        for m in range(0, 100):
            arr = [random.random() for x in range(0, 20)]
            label = classes[random.random() > 0.5]
            arrs.append(arr)
            labels.append(label)
        ann = Ann(arrs, labels, n_h=2)  # Create Ann with these train_examples and labels
        # L-1 matrices of partial derivatives for first example
        J = ann.backward_batch()
        T_original = copy.deepcopy(ann.Thetas)
         
        for l in range(0, ann.L - 1):
            shape_J = J[l].shape
            eps = 0.0001  # epsilon for a numerical approximation of the gradient
            a = random.sample(range(0, shape_J[0]), 2)
            b = random.sample(range(0, shape_J[1]), 2)
            for i in a:
                for j in b:
                    T_e = np.zeros(shape_J)  # Matrix of zeros
                    T_e[i][j] = eps
                    ann.Thetas[l] = T_original[l] + T_e
                    cost_e = ann.cost()  # Cost at Theta + eps
                    ann.Thetas[l] = T_original[l] - T_e
                    cost_minus_e = ann.cost()  # Cost at Theta - eps
                    P = (cost_e - cost_minus_e) / (2 * eps)  # Numerical approximation
                    J_ij = J[l].item(i, j)  # Backpropagation derivation
                     
                    self.assertAlmostEqual(P, J_ij, delta=0.001)
                    ann.Thetas = copy.deepcopy(T_original)
                
    @timeit     
    def test_5(self):
        # Comprehensive gradient checking #
         
        # Medium size data-set with more than two classes
        arrs = []
        labels = []
        classes = ('cat', 'dog', 'bird', 'turtle', 'dinosaur', 'human')
        for m in range(0, 100):
            arr = [random.random() for x in range(0, 200)]
            z = random.random()
            if (z < 1 / 6):
                label = classes[0]
            elif (z >= 1 / 6 and z < 2 / 6):
                label = classes[1]
            elif (z >= 2 / 6 and z < 3 / 6):
                label = classes[2]
            elif (z >= 3 / 6 and z < 4 / 6):
                label = classes[3]
            elif (z >= 4 / 6 and z < 5 / 6):
                label = classes[4]   
            else:
                label = classes[5]
            arrs.append(arr)
            labels.append(label)
        ann = Ann(arrs, labels, n_h=2)  # Create Ann with these train_examples and labels
        # L-1 matrices of partial derivatives for first example
        J = ann.backward_batch()
        T_original = copy.deepcopy(ann.Thetas)
         
        # Just check the neuron connections between first, second, and third layer
        for l in range(0, 2):
            shape_J = J[l].shape
            eps = 0.0001  # epsilon for a numerical approximation of the gradient
            # Randomly select 100 neuron connections to check
            a = random.sample(range(0, shape_J[0]), 10)
            b = random.sample(range(0, shape_J[1]), 10)
            for i in a:
                for j in b:
                    T_e = np.zeros(shape_J)  # Matrix of zeros
                    T_e[i][j] = eps
                    ann.Thetas[l] = T_original[l] + T_e
                    cost_e = ann.cost()  # Cost at Theta + eps
                    ann.Thetas[l] = T_original[l] - T_e
                    cost_minus_e = ann.cost()  # Cost at Theta - eps
                    P = (cost_e - cost_minus_e) / (2 * eps)  # Numerical approximation
                    J_ij = J[l].item(i, j)  # Backpropagation derivation
                     
                    self.assertAlmostEqual(P, J_ij, delta=0.001)
                    ann.Thetas = copy.deepcopy(T_original)
    
    @timeit    
    def non_test_6(self):
        # Test if training works by checking that training lowers the cost for random small and medium size data-sets#
         
        # Small size random data-set with two labels
        arrs = []
        labels = []
        classes = ('cat', 'dog')
        for i in range(0, 1):
            print('\nTesting data-set ' + str(i))
            for m in range(0, 10):
                arr = [random.random() for x in range(0, 3)]
                label = classes[random.random() > 0.5]
                arrs.append(arr)
                labels.append(label)
            ann = Ann(arrs, labels)  # Create Ann with these train_examples and labels
            cost_before = ann.cost()
            ann.train()
            cost_after = ann.cost()
            self.assertTrue(cost_after <= cost_before)
             
        # Medium size random data-set with three labels
        arrs = []
        labels = []
        classes = ('cat', 'dog', 'bird')
        for i in range(0, 1):
            print('\nTesting data-set ' + str(i))
            for m in range(0, 10):
                arr = [random.random() for x in range(0, 5)]
                z = random.random()
                if (z < 0.33):
                    label = classes[0]
                elif (z >= 0.33 and z < 0.66):
                    label = classes[1]
                else:
                    label = classes[2]
                arrs.append(arr)
                labels.append(label)
            ann = Ann(arrs, labels)  # Create Ann with these train_examples and labels
            cost_before = ann.cost()
            ann.train()
            cost_after = ann.cost()
            self.assertTrue(cost_after <= cost_before)
    
    @timeit     
    def test_7(self):
        # Learn some basic functions#
        # Linearly-separable data-sets#
         
        # function 1 (AND function) on 0 hidden layers
        arrs = []
        arrs.append([0, 0])
        arrs.append([0, 1])
        arrs.append([1, 0])
        arrs.append([1, 1])
        labels = []
        labels.append('false')
        labels.append('true')
        labels.append('true')
        labels.append('true') 
        ann = Ann(arrs, labels, n_h=0)
        ann.train()
        ann.validate_train()
        # Check to see if train_accuracy is over 90%
        self.assertTrue(ann.train_accuracy() > 0.9)
        # function 2 on 2 hidden layers
        arrs = []
        arrs.append([1, 1])
        arrs.append([2, 2])
        arrs.append([1, 3])
        arrs.append([2, 10])
        arrs.append([1, -1])
        arrs.append([-2, -2])
        arrs.append([1, -3])
        arrs.append([-2, -10])
        labels = []
        labels.append('false')
        labels.append('false')
        labels.append('false')
        labels.append('false')
        labels.append('true')
        labels.append('true')
        labels.append('true')
        labels.append('true') 
        ann = Ann(arrs, labels, n_h=2)
        ann.train()
        ann.validate_train()
        # Check to see if train_accuracy is over 90%
        self.assertTrue(ann.train_accuracy() > 0.9)
         
         
        # Non-linearly-separable data-sets#
         
        
        # function 1 (XOR function) on 1 hidden layers
        arrs = []
        arrs.append([0, 0])
        arrs.append([0, 1])
        arrs.append([1, 0])
        arrs.append([1, 1])
        labels = []
        labels.append('false')
        labels.append('true')
        labels.append('true')
        labels.append('false') 
        ann = Ann(arrs, labels, n_h=1)
        ann.train(it=3000)
        ann.validate_train()
        # Check to see if train_accuracy is over 90%
        self.assertTrue(ann.train_accuracy() > 0.9)
         
        # function 1b (XOR function) on 1 hidden layers (with custom architecture)
        arrs = []
        arrs.append([0, 0])
        arrs.append([0, 1])
        arrs.append([1, 0])
        arrs.append([1, 1])
        labels = []
        labels.append('false')
        labels.append('true')
        labels.append('true')
        labels.append('false')
        s = [4, 5]  # Custom hidden layer architecture
        ann = Ann(arrs, labels, n_h=len(s), s=s)
        ann.train()
        ann.validate_train()
        # Check to see if train_accuracy is over 90%
        self.assertTrue(ann.train_accuracy() > 0.9)
             
 
        # function 1 (two nested sets) on 2 hidden layers
        arrs = []
        arrs.append([0, 0])
        arrs.append([0, 1])
        arrs.append([1, 1])
        arrs.append([1, 1])
        arrs.append([10, 0])
        arrs.append([0, 10])
        arrs.append([110, 10])
        arrs.append([-10, 10])
        labels = []
        labels.append('false')
        labels.append('false')
        labels.append('false')
        labels.append('false') 
        labels.append('true')
        labels.append('true')
        labels.append('true')
        labels.append('true') 
        ann = Ann(arrs, labels, n_h=0)
        ann.train()
        ann.validate_train()
        # Check to see if train_accuracy is over 90%
        self.assertTrue(ann.train_accuracy() > 0.9)
         
    @timeit
    def test_8(self):
        # First test#
        # 1 hidden layer cost test with regularization#       
        x1 = [1, 2, 3, 4]  # Array as first example
        y1 = 'yes'
        arrs = []
        labels = []
        arrs.append(x1)
        labels.append(y1)
        ann1 = Ann(arrs, labels, n_h=1)  # Create this architecture
         
        # Custom Thetas weights#
        M1 = np.matrix([[1, -1, 0.5, -0.3, 2],
                       [1, -1, 0.5, -0.3, 2],
                       [1, -1, 0.5, -0.3, 2],
                       [1, -1, 0.5, -0.3, 2]])
        M2 = np.matrix([[1, 1, -1, 0.5, -1]])
        ann1.Thetas[0] = M1
        ann1.Thetas[1] = M2
        cost_0 = ann1.cost()  # lam equals 0
        cost_1 = ann1.cost(lam=1)  # lam equals 1
        self.assertTrue(cost_1 > cost_0)  # Cost with regularization penalty is always higher than without regularization        
 
        # Gradient checking (now with regularization)#
        # Medium size data-set with several train_examples
        lam_test = 1  # Regularization parameter
        arrs = []
        labels = []
        classes = ('cat', 'dog')
        for m in range(0, 100):
            arr = [random.random() for x in range(0, 40)]
            label = classes[random.random() > 0.5]
            arrs.append(arr)
            labels.append(label)
        ann = Ann(arrs, labels, n_h=2)  # Create Ann with these train_examples and labels
        # L-1 matrices of partial derivatives for first example
        J = ann.backward_batch(lam=lam_test, batch_size=1)  # Use full-batch for gradient descent
        T_original = copy.deepcopy(ann.Thetas)
         
        for l in range(0, ann.L - 1):
            shape_J = J[l].shape
            eps = 0.0001  # epsilon for a numerical approximation of the gradient
            a = random.sample(range(0, shape_J[0]), 2)
            b = random.sample(range(0, shape_J[1]), 2)
            for i in a:
                for j in b:
                    T_e = np.zeros(shape_J)  # Matrix of zeros
                    T_e[i][j] = eps
                    ann.Thetas[l] = T_original[l] + T_e
                    cost_e = ann.cost(lam=lam_test)  # Cost at Theta + eps
                    ann.Thetas[l] = T_original[l] - T_e
                    cost_minus_e = ann.cost(lam=lam_test)  # Cost at Theta - eps
                    P = (cost_e - cost_minus_e) / (2 * eps)  # Numerical approximation
                    J_ij = J[l].item(i, j)  # Backpropagation derivation
                     
                    # print(P, '\t', J_ij, '\t', abs(P - J_ij), (l, i, j))
                     
                    # if (P < 0 and J_ij > 0 or P > 0 and J_ij < 0):
                    #    self.fail()
                     
                    self.assertAlmostEqual(P, J_ij, delta=0.001)
                    ann.Thetas = copy.deepcopy(T_original)
 
    @timeit
    def test_9(self):
        # function 1 (XOR function) on 1 hidden layers
        arrs = []
        arrs.append([0, 0])
        arrs.append([0, 1])
        arrs.append([1, 0])
        arrs.append([1, 1])
        labels = []
        labels.append('false')
        labels.append('true')
        labels.append('true')
        labels.append('false') 
        ann = Ann(arrs, labels, n_h=1)
        # Train and save model
        model = ann.train()[0][0]  # Take the first model from the list of models in the tuple
        ann.validate_train()
        # Check to see if train_accuracy is over 90%
        self.assertTrue(ann.train_accuracy() > 0.9)
         
        # Load the trained model into a new neural network
        ann_from_model = Ann(model)
        # Evaluate some vectors using this neural network initialized only with a model
        self.assertEqual(ann_from_model.h_by_class(arrs[0]), 'false')
        self.assertEqual(ann_from_model.h_by_class(arrs[1]), 'true')
        x = [1.1, 0.9]
        self.assertEqual(ann_from_model.h_by_class(x), 'false')
 
        # function 2 on 2 hidden layers
        arrs2 = []
        arrs2.append([1, 1])
        arrs2.append([2, 2])
        arrs2.append([1, 3])
        arrs2.append([2, 10])
        arrs2.append([1, -1])
        arrs2.append([-2, -2])
        arrs2.append([1, -3])
        arrs2.append([-2, -10])
        labels2 = []
        labels2.append('false')
        labels2.append('false')
        labels2.append('false')
        labels2.append('false')
        labels2.append('true')
        labels2.append('true')
        labels2.append('true')
        labels2.append('true') 
        ann = Ann(arrs2, labels2, n_h=2)
        model2 = ann.train()[0][0]
        ann.validate_train()
         
        # Load the second model
        ann_from_model = Ann(model2)
        # Evaluate some vectors using this neural network initialized only with a model
        self.assertEqual(ann_from_model.h_by_class(arrs2[0]), 'false')
        self.assertEqual(ann_from_model.h_by_class(arrs2[len(arrs2) - 1]), 'true')
        x = [1, -5]
        self.assertEqual(ann_from_model.h_by_class(x), 'true')
         
        # Load the first model again
        ann_from_model = Ann(model)
        # Evaluate some vectors using this neural network initialized only with a model
        self.assertEqual(ann_from_model.h_by_class(arrs[0]), 'false')
        self.assertEqual(ann_from_model.h_by_class(arrs[1]), 'true')
        x = [1.1, 0.9]
        self.assertEqual(ann_from_model.h_by_class(x), 'false')
         
        # Try pickling our model into a sister folder
        model_name = model.name
        directory = '../Ann-models'
        path_to_file = directory + '/' + model_name
        if not os.path.exists(directory):
            os.makedirs(directory)
        pickle.dump(model, open(path_to_file, 'wb'))
         
        # Try unpickling our model
        unpickled_model = pickle.load(open(path_to_file, 'rb'))
        # Load unpickled model and test
        ann_from_pickle = Ann(unpickled_model)
        # Evaluate some vectors using this neural network initialized only with a model
        self.assertEqual(ann_from_pickle.h_by_class(arrs[0]), 'false')
        self.assertEqual(ann_from_pickle.h_by_class(arrs[1]), 'true')
        x = [1.1, 0.9]
        self.assertEqual(ann_from_pickle.h_by_class(x), 'false')
     
    @timeit
    def test_10(self):
        '''Creates a fake data-set with points labeled 'yes' around origin and points labeled 'no' outside'''
        arrs = []
        labels = []
        '''Points about the origin (located in a box of length 16 centered at origin)'''
        for i in range(0, 10):
            arr = [random.randint(0, 8) * np.sign(random.random() - 0.5) for x in range(0, 2)]
            label = 'yes'
            arrs.append(arr)
            labels.append(label)
        '''Points outside the box'''
        for i in range(0, 10):
            arr = [random.randint(10, 20) * np.sign(random.random() - 0.5) for x in range(0, 2)]
            label = 'no'
            arrs.append(arr)
            labels.append(label)
        '''Add some noise'''
        for i in range(0, 2):
            arr = [random.randint(0, 8) * np.sign(random.random() - 0.5) for x in range(0, 2)]
            label = 'no'  # Note: this is artificially misclassified
            arrs.append(arr)
            labels.append(label)
        for i in range(0, 10):
            arr = [random.randint(10, 20) * np.sign(random.random() - 0.5) for x in range(0, 2)]
            label = 'yes'  # Note: this is artificially misclassified
            arrs.append(arr)
            labels.append(label)
             
        ann = Ann(arrs, labels, n_h=2)
        (models, test_accuracies, test_costs) = ann.train()
         
        best_test_accuracy = 0
        best_i = -1
        for i in range(0, len(test_accuracies)):
            if (test_accuracies[i] > best_test_accuracy):
                best_test_accuracy = test_accuracies[i]
                best_i = i
                 
        if (best_i > -1):
            model_name = models[i].name
            directory = '../Ann-models'
            path_to_file = directory + '/' + model_name
            if not os.path.exists(directory):
                os.makedirs(directory)
            pickle.dump(models[i], open(path_to_file, 'wb'))
        else:
            logger.error('Error!')
    
if __name__ == "__main__":
    Ann.init_logger('debug')
    unittest.main()
