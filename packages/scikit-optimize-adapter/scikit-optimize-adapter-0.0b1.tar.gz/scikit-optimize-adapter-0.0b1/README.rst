

Scikit-Optimize-Adapter
=======================


Scikit-Optimize-Adapter (Adapter: "A DAsk Parallel TunER") is an efficient light weight library built on top of Scikit-Optimize and Dask that lets the user do Bayesian optimization hyperparameter tuning with different schemes of parallelized cross-validations.


Install
-------

::

	pip install --index-url https://test.pypi.org/simple/ --no-deps scikit-optimize-adapter --upgrade


Getting started
---------------

Let's start with the below dummy training data:

.. code:: python

	import pandas as pd
	import numpy as np

	data = np.arange(30*4).reshape(30, 4)
	df = pd.DataFrame(data=data, columns=['target', 'f1', 'f2', 'f3'])

	features = ['f1', 'f2', 'f3']
	target = 'target'

	K = 5

	orderby=None
	num_partition=None
	window_size=None

	from skopt.space import Space, Categorical, Integer, Real, Dimension

	space  = [Real(0.5, 10),      # learning rate       (learn_rate)
	          Real(0, 1),         # gamma               (min_split_improvement)
	          Integer(3, 4),      # max_depth           (max_depth)
	          Integer(11, 13),    # n_estimators        (ntrees)
	          Integer(2, 4),      # min_child_weight    (min_rows)
	          Real(0, 1),         # colsample_bytree    (col_sample_rate_per_tree)
	          Real(0, 1)]         # subsample           (sample_rate)


Adapter is shipped with XGBoost regressor and classifier, but you can pass in a callable estimator of your design if you wish to customize it. 

.. code:: python

	from adapter import Adapter

	adapt = Adapter(df, features, target, K, groupby=None, 
                cross_validation_scheme='random_shuffle',
                search_method="bayesian_optimization",
                estimator="xgboost_regression")  # "xgboost_regression" or "xgboost_classification" or callable estimator (more on this later)

Try copying the link to the web browser to check out the dask dashboard: ``http://127.0.0.1:8789/status``.

You can visualize the Dask delayed computation graph:

.. code:: python

	delayed_graph = adapt.construct_delayed_graph(num_iter=3, search_space=space)  # we will set n_iter to 3 to make visualizing manageable. 
	delayed_graph.visualize()

.. figure:: https://github.com/mozjay0619/scikit-optimize-adapter/blob/master/media/graph.png

Let's run the code. ``num_initial`` is the number of random initial searches and ``num_iter`` is the total number of search steps taken, including the ``num_initial`` step counts. (Example: ``num_initial=5, num_iter=15`` means 5 random search and 10 Bayesian search)

.. code:: python

	res = adapt.run(num_initial=5, num_iter=15, search_space=space)

While it runs, checkout the dashboard again, and click on the ``Graph`` tab. You will see the above computation graph being worked on in real time!

.. figure:: https://github.com/mozjay0619/scikit-optimize-adapter/blob/master/media/daskdashboard.png


Now you can retrieve the results:

.. code:: python

	adapt.plot_improvements()  # to show the improvements 
	optimal_params = adapt.get_optimal_params()  # which you can use to train your final model

.. figure:: https://github.com/mozjay0619/scikit-optimize-adapter/blob/master/media/improvement.png

If you are running this in a local machine, you must take responsibility of removing the temporary directory:

.. code:: python

	adapt.cleanup()


Cross-validation schemes
------------------------

There are 5 different cross-validation schemes supported by the adapter:

* ``random_shuffle``: create K cross-validation folds from randomly shuffled rows
	- Default mode for most regression tasks .
* ``ordered``: create K cross-validation folds after sorting the train data by a certain column
	- Used for regression tasks where data has time series nature with high temporal auto-correlation.
	- Must supply ``orderby`` argument.
* ``binary_classification``: create K cross-validation folds where positive/negative label proportion is preserved
	- Used for classification task.
	- This mode will preserve the positive and negative label proportions in each fold.
* ``stratified_sampling``: create K cross-validation folds such that the skew distribution of response is preserved 
	- Used for regression task where the continuous response variable is highly skewed.
	- This mode will preserve the skew distribution of the response values by sampling from stratification.
	- Must supply ``num_partition`` argument.
* ``expanding_window``: mainly for time series modeling 
	- Refer to:


Tuning for multiple models in parallel
--------------------------------------

Again, let's take a look at a specific example data:

.. code:: python

	import pandas as pd
	import numpy as np

	group_col = np.asarray([1]*10 + [2]*10 + [3]*10 + [4]*10 + [5]*10 + [6]*10).reshape(-1, 1)  # this time we have a column specifying group
	data = np.arange(60*4).reshape(60, 4)
	data = np.hstack((data, group_col))
	df = pd.DataFrame(data=data, columns=['target', 'f1', 'f2', 'f3', 'groups'])

	features = ['f1', 'f2', 'f3']
	target = 'target'

	K = 5

	orderby=None
	num_partition=None
	window_size=None

	from skopt.space import Space, Categorical, Integer, Real, Dimension

	space  = [Real(0.5, 10),      # learning rate       (learn_rate)
	          Real(0, 1),         # gamma               (min_split_improvement)
	          Integer(3, 4),      # max_depth           (max_depth)
	          Integer(11, 13),    # n_estimators        (ntrees)
	          Integer(2, 4),      # min_child_weight    (min_rows)
	          Real(0, 1),         # colsample_bytree    (col_sample_rate_per_tree)
	          Real(0, 1)]         # subsample           (sample_rate)

We can tune the models for each group by passing by ``groupby`` argument. 

.. code:: python

	from adapter import Adapter

	adapt = Adapter(df, features, target, K, groupby='groups', 
                cross_validation_scheme='random_shuffle',
                search_method="bayesian_optimization",
                estimator="xgboost_regression")  

Run the adapter the same way:

.. code:: python

	res = adapt.run(num_initial=5, num_iter=15, search_space=space)

You can visualize the Dask delayed computation graph:

.. figure:: https://github.com/mozjay0619/scikit-optimize-adapter/blob/master/media/multigraph_dashboard.png


Passing in an arbitrary callable estimator
------------------------------------------

You can pass in an arbitrary callable estimator as long as it implements the standard scikit-learn estimator API: 

.. code:: python

	from abc import ABCMeta, abstractmethod

	class BaseEstimator(object, metaclass=ABCMeta):
	    """
	    Base class for all Algorithm classes.
	    """

	    def __init__(self, **kwargs):
	        pass
	     
	    @abstractmethod
	    def fit(self, X, y, params):
	        pass

	    @abstractmethod
	    def score(self, X, y):
	        pass

	    @abstractmethod
	    def predict(self, X):
	        pass 
       
For example, we can even do something like:

.. code:: python

	from adapter import BaseEstimator  # import BaseEstimator!

	class DummyEstimator(BaseEstimator):
	    
	    def __init__(self):
	        pass
	    
	    def fit(self, train_X, train_y, params):
	        a = len(train_X)/10.
	        
	        for i in range(int(a*5000000)):
	            i + 1
	        
	        print(len(train_X), len(train_y))
	        
	    def score(self, validation_X, validation_y):
	        
	        print(len(validation_X), len(validation_y))
	        
	        return 1.5
	    
	    def predict(self, test_X):
	        
	        return len(test_X)

	my_estimator = DummyEstimator()

Then you can use it with the Adapter:

.. code:: python

	from adapter import Adapter

	adapt = Adapter(df, features, target, K, groupby='groups', 
                cross_validation_scheme='random_shuffle',
                search_method="bayesian_optimization",
                estimator=my_estimator)  # your own estimator


Tuning multiple models with highly skewed training data sizes
-------------------------------------------------------------

When the data size for each group is highly skewed, a suboptimal resource allocation can occur. In this case, it is more advantageous to throttle the feeding of delayed graphs to the Dask client by using multiple thread instances. Let's again look at an example case:

.. code:: python

	import pandas as pd
	import numpy as np
	import time

	group_col = np.asarray([1]*100 + [2]*2 + [3]*2 + [4]*2 + [5]*2 + [6]*2 + [7]*2 + [8]*2 + [9]*2 + [16]*2 + [26]*2 + [17]*2 + [18]*2 + [19]*2 + [116]*2 + [126]*2).reshape(-1, 1)
	data = np.arange(130*4).reshape(130, 4)
	data = np.hstack((data, group_col))
	df = pd.DataFrame(data=data, columns=['target', 'f1', 'f2', 'f3', 'groups'])

	features = ['f1', 'f2', 'f3']
	groupby = 'groups'
	target = 'target'

	K = 5

	from adapter import BaseEstimator  # import BaseEstimator!

	class DummyEstimator(BaseEstimator):

	    def __init__(self):
	        pass

	    def fit(self, train_X, train_y, params):
	        a = len(train_X)/10.

	        for i in range(int(a*5000000)):
	            i + 1

	        print(len(train_X), len(train_y))

	    def score(self, validation_X, validation_y):

	        print(len(validation_X), len(validation_y))

	        return 1.5

	    def predict(self, test_X):

	        return len(test_X)

	my_estimator = DummyEstimator()

	orderby=None
	num_partition=None
	window_size=None

	from skopt.space import Space, Categorical, Integer, Real, Dimension

	space  = [Real(0.5, 10),      # learning rate       (learn_rate)
	          Real(0, 1),         # gamma               (min_split_improvement)
	          Integer(3, 4),      # max_depth           (max_depth)
	          Integer(11, 13),    # n_estimators        (ntrees)
	          Integer(2, 4),      # min_child_weight    (min_rows)
	          Real(0, 1),         # colsample_bytree    (col_sample_rate_per_tree)
	          Real(0, 1)]         # subsample           (sample_rate)

In such a case, we use ``run_with_threads`` method call, where we pass an additional argument of ``num_threads``:

.. code:: python

	from adapter import Adapter

	adapt = Adapter(df, features, target, K, groupby='groups',
	        cross_validation_scheme='random_shuffle',
	        search_method="bayesian_optimization",
	        estimator=my_estimator)  # your own estimator

	res = adapt.run(num_initial=5, num_iter=15, search_space=space, num_threads=2)  # num_threads

You can check fromt the Dask dashboard that only two delayed computation graphs are worked on at the same time, achieving a dynamic resource allocation in effect:

.. figure:: https://github.com/mozjay0619/scikit-optimize-adapter/blob/master/media/twograph_dashboard.png



Todo:

1. rest of the cross validation schemes
2. testing hard thresholded submit process (and testing speed without it)
3. supervised encodings
4. add unit tests
5. continuous integration set up
6. random search method
7. multi GPU environment
8. documentations
9. ~~getting the results of the optimization~~
10. ~~visualization of optimizations~~
11. early stop criterion using callbacks
12. ~~beta readme.rst for install and tutorial~~
13. full readme.rst for install and tutorial
14. periodic training 
15. bayesian warm start training
16. dependency managements
17. active per worker threadpool managements



