IPython Parallel

3rd ed - changes

In [8]: dview.execute("import sys")
   ...: 
Out[8]: <AsyncResult(execute): pending>

In [9]: dview.push({'shared_data': [50, 100]})
Out[9]: <AsyncResult(_push): pending>

...

In [1]: %run pi_ipython_cluster.py
We're using 4 engines
Estimates made: [19633556, 19637444, 19635854, 19632938]
Estimated pi 3.14159168
Delta: 24.4925217628479




IPython Parallel

$ ipcluster start -n 4
2019-12-14 18:12:55.535 [IPClusterStart] Starting ipcluster with [daemon=False]
2019-12-14 18:12:55.536 [IPClusterStart] Creating pid file: /home/ian/.ipython/profile_default/pid/ipcluster.pid
2019-12-14 18:12:55.536 [IPClusterStart] Starting Controller with LocalControllerLauncher
2019-12-14 18:12:56.540 [IPClusterStart] Starting 4 Engines with LocalEngineSetLauncher
2019-12-14 18:13:26.862 [IPClusterStart] Engines appear to have started successfully


In [1]: import ipyparallel as ipp                                                                                                                                                                                                             
In [2]: c=ipp.Client()                                                                                                                                                                                                                        
In [3]: print(c.ids)                                                                                                                                                                                                                          
[0, 1, 2, 3]

In [4]: c[:].apply_sync(lambda: "Hello High Performance Pythonistas!")                                                                                                                                                                        
Out[4]: 
['Hello High Performance Pythonistas!',
 'Hello High Performance Pythonistas!',
 'Hello High Performance Pythonistas!',
 'Hello High Performance Pythonistas!']


In [5]: dview=c[:]                                                                                                                                                                                                                            
In [6]: with dview.sync_imports(): 
   ...:     import os 
importing os on engine(s)

In [7]: dview.apply_sync(lambda: os.getpid())                                                                                                                                                                                                 
Out[7]: [16158, 16159, 16160, 16163]

In [8]: dview.execute("import sys")                                                                                                                                                                                                           
In [9]: dview.push({'shared_data': [50, 100]})                                                                                                                                                                                               
In [10]: dview.apply_sync(lambda: len(shared_data))                                                                                                                                                                                           
Out[10]: [2, 2, 2, 2]


In [29]: %run pi_ipython_cluster.py                                                                                                                                                                                                           
We're using 4 engines
Estimates made: [19636752, 19634225, 19635101, 19638841]
Estimated pi 3.14179676
Delta: 20.68650197982788

## Dask and Swifter

See pandas/ols_basics/ and the chapter recipe and demo there
