import numpy as np
from scipy import optimize as opt
import math

def normalize(X):
    X_norm = X
    mu = np.zeros((1,X.shape[1]))
    sigma = np.zeros((1,X.shape[1]))
    for i in range(X.shape[1]):
        mu[:,i] = np.mean(X[:,i])
        sigma[:,i] = np.std(X[:,i])
        X[:,i] = (X[:,i] - mu[:,i]) / sigma[:,i]
    return (X_norm, mu, sigma)

def sigmoid(X):
    sig = 1 / (1 + np.exp(-X))
    ep = 0.000001
    for x in np.nditer(sig, op_flags=['readwrite']):        
        if x == 1:
            x -= ep
        elif x == 0:
            x += ep
    return sig

def costFunction(theta, X, y, lam):
    m = X.shape[0]
    h = sigmoid(X.dot(theta))
    print(h)
    log10 = np.vectorize(math.log10) #makes log10 useable on numpy arrays
    J = (1/m) * np.sum(-y*log10(h) - (1-y)*log10(1-h)) + (lam/(2*m)) * np.sum(theta[1:]**2)
    return J

def costFunctionGrad(theta, X, y, lam):
    m = X.shape[0]
    h = sigmoid(X.dot(theta))
    temp_theta = theta
    temp_theta[0] = 0
    grad = (1/m) * X.T.dot(h-y) + (lam/m) * temp_theta
    return grad

def trainOneVsAll(X, y, num_labels, lam):
    m = X.shape[0]
    n = X.shape[1]
    X, mu, sigma = normalize(X)
    X = np.c_[np.ones(m), X]
    all_theta = np.zeros((num_labels, n+1))
    initial_theta = np.zeros(n+1)

    for i in range(num_labels):
        min_theta = opt.fmin_bfgs(costFunction, initial_theta, args=(X,y==i,lam))
        all_theta[i,:] = min_theta
    return (all_theta, mu, sigma)

def predictOneVsAll(all_theta, X):
    p = np.zeros(X.shape[0])
    X = np.c_[np.ones(X.shape[0]), X]
    print(all_theta)
    print(sigmoid(X.dot(all_theta.T)))
    p = np.argmax(sigmoid(X.dot(all_theta.T))[0])
    return p
