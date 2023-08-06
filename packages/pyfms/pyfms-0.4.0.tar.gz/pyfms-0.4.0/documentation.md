﻿Documentation
-------------

To use `pyfms`, first import the module.

    >>> import pyfms
    
### Initializing a Model

A factorization machine is created with *pyfms.Classifier* for a binary classification problem, or
*pyfms.Regressor* for regression. The constructors require an argument specifying the number of features.

    >>> model = pyfms.Regressor(feature_count)

pyfms.Regressor and pyfms.Classifier both take the following arguments:

* **feature_count** The dimensionality of each data point.
* **k** (optional; defaults to 8) Dimensionality of the factorization of pairwise interactions.
* **stdev** (optional; defaults to .01) The standard deviation of the normal distribution used to initialize the
interaction parameters of the model.
* **X_format** (optional; defaults to "dense") The format of the feature matrices (for training and prediction).
Dense data is supported with "dense". Sparse data is supported with "csr" (compressed sparse row) or "csc"
(compressed sparse column).
    
### Training a Model

A factorization machine is trained with the *fit* method, which takes as input a training dataset X, and a vector of
target values. For binary classification, the target values must be 1 or 0.

    >>> model.fit(X, y)

*fit* takes the following arguments:

* **X** An *n-by-d* numpy.ndarray with training data. The rows correspond to observations, and the columns correspond to
dimensions.
* **y** A numpy.ndarray vector with *n* target values corresponding to the *n* data points in *X*.
* **optimizer** (optional; defaults to *pyfms.optimizers.Adam()*) An object of a class that extends
*pyfms.core.Optimizer*, which specifies how to optimize the loss function.
* **regularizer** (optional; defaults to None) An object of a class that extends *pyfms.core.Regularizer*, which
specifies how to regularize the loss function. For example, see *L1* or *L2* in *regularizers.py*.
* **sample_weight** (optional; defaults to None) A numpy.ndarray vector with *n* sample weights corresponding to the
*n* data points in *X*.
* **batch_size** (optional; defaults to 128) Number of samples per gradient update.
* **nb_epoch** (optional; defaults to 100)  The number of epochs to train the model.
* **shuffle** (optional; defaults to True) A flag indicating whether to shuffle the training samples at each epoch.
* **verbosity** (optional; defaults to 0) An integer specifying the interval between logging details to stdout when
training the model. A non-positive integer suppresses logging. Increasing the value decreases the rate of output.
* **memory** (optional; defaults to True) If False, the last set of weights from training will be retained. If True,
the set of weights that minimized the loss function (across epochs) will be retained.

### Predicting with a Factorization Machine

For regression models, *predict* can be used to predict the regression targets for a dataset X.

    >>> model.predict(X)

For binary classification models, *predict* can be used to predict the class targets for a dataset X. *predict_proba*
returns the class 1 probability for a dataset X.

    >>> model.predict(X)
    >>> model.predict_proba(X)

*predict* and *predict_proba* take the following argument:

* **X** An *n-by-d* numpy.ndarray with data. The rows correspond to observations, and the columns correspond to
dimensions.

### Saving a Factorization Machine

A factorization machine is saved with the *save_weights* method, which takes as input a filename.

    >>> model.save_weights("/path/to/model.fm")

*save_weights* takes the following argument:

* **path** The file path for saving the model weights.

### Loading a Saved Factorization Machine

A saved factorization machine can be loaded with the *load_weights* method.
    
    >>> model = pyfm.FactorizationMachineRegressor(feature_count)
    >>> model.load_weights("/path/to/model.fm")

*load_weights* takes the following argument:

* **path** The file path for loading the model weights.
