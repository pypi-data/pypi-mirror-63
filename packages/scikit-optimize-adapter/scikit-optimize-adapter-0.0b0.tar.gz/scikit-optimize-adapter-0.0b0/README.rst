

Scikit-Optimize-Adapter
=======================


Scikit-Optimize-Adapter (Adapter: "A DAsk Parallel TunER") is an efficient light weight library built on top of Scikit-Optimize and Dask that lets the user do Bayesian optimization hyperparameter tuning with different schemes of parallelized cross-validations.


Install
-------

::

	pip install --index-url https://test.pypi.org/simple/ --no-deps scikit-optimize-adapter --upgrade


Getting started
---------------

This is a very quick and basic tutorial. More detailed tutorials will be written soon!

Let's start with the below dummy training data:

.. code:: python

	import pandas as pd
	import numpy as np

	group_col = np.asarray([1]*10 + [2]*10 + [3]*10).reshape(-1, 1)
	data = np.arange(30*4).reshape(30, 4)
	data = np.hstack((data, group_col))
	df = pd.DataFrame(data=data, columns=['target', 'f1', 'f2', 'f3', 'groups'])

	features = ['f1', 'f2', 'f3']
	groupby = 'groups'
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
                estimator="xgboost_regression")

Try copying the link to the web browser to check out the dask dashboard: ``http://127.0.0.1:8789/status``.

You can visualize the Dask delayed computation graph:

.. code:: python

	delayed_graph = adapt.construct_delayed_graph(num_iter=3, search_space=space)  # we will set n_iter to 3 to make visualizing manageable. 
	delayed_graph.visualize()

.. figure:: https://github.com/mozjay0619/scikit-optimize-adapter/blob/master/media/graph.png

Let's run the code: 

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



