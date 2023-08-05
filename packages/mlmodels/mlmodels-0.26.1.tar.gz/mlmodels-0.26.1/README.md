# mlmodels : Model ZOO for Pytorch, Tensorflow, Keras, Gluon models...

* Model ZOO with Lightweight Functional interface to wrap access to Recent and State o Art Deep Learning, ML models and Hyper-Parameter Search, cross platforms such as Tensorflow, Pytorch, Gluon, Keras,...

* Logic follows sklearn API: fit, predict, transform, metrics, save, load

* Goal is to transform Jupyter code into Semi-Prod code with minimal code change ... 

* Model list is available here : 
  https://github.com/arita37/mlmodels/blob/dev/README_model_list.md

* Why Functional interface instead of OOP ?
    Just Functional reduces the amount of code needed, focus more on the computing part (vs design part), 
    a bit easier maintenability for medium size project, good for scientific computing process.


```
#### Docs here:   https://mlmodels.readthedocs.io/en/latest/  (incomplete docs)
```

######################################################################################

## ① Installation
Install as editable package (ONLY dev branch), in Linux
    conda create -n py36 python=3.6.5  -y
    source activate py36

    cd yourfolder
    git clone https://github.com/arita37/mlmodels.git mlmodels
    cd mlmodels
    git checkout dev 


    ### On Linux/MacOS    
    pip install numpy<1.17.0
    pip install -e .  -r requirements.txt


    ### On Windows 
    VC 14   https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2019
    pip install  numpy<1.17.0
    pip install torch==0.4.1 -f https://download.pytorch.org/whl/torch_stable.html   
    pip install -e .  -r requirements_wi.txt  


    ### No Deps
    # pip install -e .  --no-deps    



    ##### To test :
    ml_optim

    ##### To test model fitting
    ml_models
    
    
    

####  Dependencies
```
requirements.txt

```

#### Actual test runs
```
https://github.com/arita37/mlmodels/actions

```

![test_fast_linux](https://github.com/arita37/mlmodels/workflows/test_fast_linux/badge.svg)

![test_fast_windows](https://github.com/arita37/mlmodels/workflows/test_fast_windows/badge.svg?branch=dev)









#######################################################################################

## ② How to add a new model
### Source code structure as below
- `docs`: documentation
- `mlmodels`: interface wrapper for pytorch, keras, gluon, tf, transformer NLP for train, hyper-params searchi.
    + `model_xxx`: folders for each platform with same interface defined in template folder
    + `dataset`: store dataset files for test runs.
    + `template`: template interface wrapper which define common interfaces for whole platforms
    + `ztest`: testing output for each sample testing in `model_xxx`
- `ztest`: testing output for each sample testing in `model_xxx`

###  How to define a custom model
#### 1. Create a file `mlmodels\model_XXXX\mymodel.py` , XXX: tch: pytorch, tf:tensorflow, keras:keras, .... 
- Declare below classes/functions in the created file:

      Class Model()                                                  :   Model definition
            __init__(model_pars, data_pars, compute_pars)            :   
                                  
      def fit(model, data_pars, model_pars, compute_pars, out_pars ) : Train the model
      def predict(model, sess, data_pars, compute_pars, out_pars )   : Predict the results
      def metric(ytrue, ypred, yproba, data_pars, compute_pars, out_pars )         : Measure the results

      def get_params(choice, data_path, config_mode)                                               : returnparameters of the model
      def get_dataset(data_pars)                                     : load dataset
      def test()                                                     : example running the model     
      def test2()                                                    : example running the model in global settings  

      def save(model, path)                                          : save the model
      def load(path)                                                 : load the trained model


- *Infos* 
     ```
     model :         Model(model_pars), instance of Model() object
     sess  :         Session for TF model  or optimizer in PyTorch
     model_pars :    dict containing info on model definition.
     data_pars :     dict containing info on input data.
     compute_pars :  dict containing info on model compute.
     out_pars :      dict containing info on output folder.
     ```

#### 2. Write your code and create test() to test your code.  **
- Declare model definition in Class Model()
```python
    self.model = DeepFM(linear_cols, dnn_cols, task=compute_pars['task']) # mlmodels/model_kera/01_deectr.py
    # Model Parameters such as `linear_cols, dnn_cols` is obtained from function `get_params` which return `model_pars, data_pars, compute_pars, out_pars`
```        
- Implement pre-process data in function `get_dataset` which return data for both training and testing dataset
Depend on type of dataset, we could separate function with datatype as below example
```python    
    if data_type == "criteo":
        df, linear_cols, dnn_cols, train, test, target = _preprocess_criteo(df, **kw)

    elif data_type == "movie_len":
        df, linear_cols, dnn_cols, train, test, target = _preprocess_movielens(df, **kw)
```
- Call fit/predict with initialized model and dataset
```python
    # get dataset using function get_dataset
    data, linear_cols, dnn_cols, train, test, target = get_dataset(**data_pars)
    # fit data
     model.model.fit(train_model_input, train[target].values,
                        batch_size=m['batch_size'], epochs=m['epochs'], verbose=2,
                        validation_split=m['validation_split'], )
    # predict data
    pred_ans = model.model.predict(test_model_input, batch_size= compute_pars['batch_size'])
```
- Calculate metric with predict output
```python
    # input of metrics is predicted output and ground truth data
    def metrics(ypred, ytrue, data_pars, compute_pars=None, out_pars=None, **kwargs):
```
- *Example* 
    https://github.com/arita37/mlmodels/tree/dev/mlmodels/template
    https://github.com/arita37/mlmodels/blob/dev/mlmodels/model_gluon/gluon_deepar.py
    https://github.com/arita37/mlmodels/blob/dev/mlmodels/model_gluon/gluon_deepar.json


#### 3. Create JSON config file inside  /model_XXX/mymodel.json  **
- Separate configure for staging development environment such as testing and production phase
then for each staging, declare some specific parameters for model, dataset and also output
- *Example*
```json
    {
        "test": {
            "model_pars": {
                "learning_rate": 0.001,
                "num_layers": 1,
                "size": 6,
                "size_layer": 128,
                "output_size": 6,
                "timestep": 4,
                "epoch": 2
            },
            "data_pars": {
                "data_path": "dataset/GOOG-year.csv",
                "data_type": "pandas",
                "size": [0, 0, 6],
                "output_size": [0, 6]
            },
            "compute_pars": {
                "distributed": "mpi",
                "epoch": 10
            },
            "out_pars": {
                "out_path": "dataset/",
                "data_type": "pandas",
                "size": [0, 0, 6],
                "output_size": [0, 6]
            }
        },
    
        "prod": {
            "model_pars": {},
            "data_pars": {}
        }
    }
```


 
#######################################################################################

## ③ CLI tools: package provide below tools
```
- ml_models    :  mlmodels/models.py
- ml_optim     :  mlmodels/optim.py
- ml_test      :  mlmodels/ztest.py


https://github.com/arita37/mlmodels/blob/dev/README_model_list.md


```
   





#######################################################################################
### ④ Interface

models.py 
```
   module_load(model_uri)
   model_create(module)
   fit(model, module, session, data_pars, out_pars   )
   metrics(model, module, session, data_pars, out_pars)
   predict(model, module, session, data_pars, out_pars)
   save(model, path)
   load(model)
```

optim.py
```
   optim(modelname="model_tf.1_lstm.py",  model_pars= {}, data_pars = {}, compute_pars={"method": "normal/prune"}
       , save_folder="/mymodel/", log_folder="", ntrials=2) 

   optim_optuna(modelname="model_tf.1_lstm.py", model_pars= {}, data_pars = {}, compute_pars={"method" : "normal/prune"},
                save_folder="/mymodel/", log_folder="", ntrials=2) 
```

#### Generic parameters 
```
   Define in models_config.json
   model_params      :  Relative to model definition 
   compute_pars      :  Relative to  the compute process
   data_pars         :  Relative to the input data
   out_pars          :  Relative to outout data
```
   Sometimes, data_pars is required to setup the model (ie CNN with image size...)
   





####################################################################################
### ⑤ Code sample

```python
https://github.com/arita37/mlmodels/blob/dev/README_model_list.md


```







#######################################################################################
### ⑥ Naming convention

### Function naming
```
pd_   :  input is pandas dataframe
np_   :  input is numpy
sk_   :  inout is related to sklearn (ie sklearn model), input is numpy array
plot_

_col_  :  name for colums
_colcat_  :  name for category columns
_colnum_  :  name for numerical columns (folat)
_coltext_  : name for text data

_stat_ : show statistics
_df_  : dataframe
_num_ : statistics

col_ :  function name for column list related.
```

### Argument Variables naming 
```
df     :  variable name for dataframe
colname  : for list of columns
colexclude
colcat : For category column
colnum :  For numerical columns
coldate : for date columns
coltext : for raw text columns
```

###############################################################################











