import numpy as np
from random import shuffle
from past.builtins import xrange

"""
Structured SVM loss function, naive implementation (with loops).

Inputs have dimension D, there are C classes, and we operate on minibatches
of N examples.

Inputs:
- W: A numpy array of shape (D, C) containing weights.
- X: A numpy array of shape (N, D) containing a minibatch of data.
- y: A numpy array of shape (N,) containing training labels; y[i] = c means
that X[i] has label c, where 0 <= c < C.
- reg: (float) regularization strength

Returns a tuple of:
- loss as single float
- gradient with respect to weights W; an array of same shape as W
"""
def svm_loss_naive(W, X, y, reg):
    dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
    num_classes = W.shape[1]
    num_train = X.shape[0]
    loss = 0.0
    for i in xrange(num_train):
        scores = X[i].dot(W)
        correct_class_score = scores[y[i]]
        for j in xrange(num_classes):
            if j == y[i]:
                continue                                 #jump over self class
            margin = scores[j] - correct_class_score + 1 # note delta = 1
            if margin > 0:
                loss += margin
                dW[:,y[i]] += -(X[i].T)
                dW[:,j] += (X[i].T)

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
    loss /= num_train
    dW /= num_train

  # Add regularization to the loss.
    loss += reg * np.sum(W * W)  # L2 regularization
    dW += reg * 2 * W

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################


    return loss, dW


"""
Structured SVM loss function, vectorized implementation.

Inputs and outputs are the same as svm_loss_naive.
"""
def svm_loss_vectorized(W, X, y, reg):
    loss = 0.0
    dW = np.zeros(W.shape) # initialize the gradient as zero

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
    scores = X.dot(W)
    correct_class_score = scores[np.arange(scores.shape[0]), y]
    margin = scores - correct_class_score.reshape(scores.shape[0], -1) + 1
    margin = np.maximum(0, margin)
    margin[np.arange(margin.shape[0]), y] = 0
    loss = np.sum(margin)/X.shape[0]

  # Add regularization to the loss.
    loss += reg * np.sum(W * W)  # L2 regularization
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
    valid_class_count = np.zeros(margin.shape)
    valid_class_count[margin > 0] = 1
    valid_class_count[np.arange(valid_class_count.shape[0]), y] -= np.sum(valid_class_count, axis=1)
    dW = (X.T).dot(valid_class_count)
    
    dW /= X.shape[0]
    dW += reg * 2 * W
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

    return loss, dW
