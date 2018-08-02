# INESCTEC-FLYINGNETWORKS
![alt text](https://imgur.com/a/Ue11FP8.png)
## What is this
This software was made over the course of a summer internship at INESC TEC Porto. Its goal is to use a machine learning to predict the performance, measured by the variables throughput, delay and pdr, of a network based on UAVs (unnamed aerial vehicles), and use that prediction to chose the UAVs location which gives the best performance.

## Dependencies
* [Python3](https://www.python.org/downloads/)
* [Keras](http://keras.io/#installation)
* [TensorFlow](https://www.tensorflow.org/install/install_sources)

## Instructions
There are 2 different scripts that should be run:

- build_model.py

Used to build the model. Can be run with command:

`python3 build_model.py`

After the model is built, 3 *.json* files are saved at **DataSet/Models-json** with the 3 models corresponding to Throughput, Delay and PDR, and 3 *.hdf5* files are saved at **DataSet/Checkpoints** with the corresponding weights. After that, you should put these files in the **DataSet** folder, and change their name to model_<QUALITY_METRIC>.json and model_<QUALITY_METRIC>.hdf5 for each corresponding file.
Note: in the case of the *hdf5* files, everytime this script runs, it generates the 3 files with names like checkpoin<NUMBER>.hdf5, so just use the 3 highest numbered files for the last model generated, being the lowest numbered the Throughput file and the highest numbered the PDR. 

- best_topology.py

Used to get the best topology for 10 predefined scenarios, representing the traffic generated by users. Can be run with command:

`python3 best_topology.py`
  
 ## Final Results
  The folder FinalResults contains some plots and excel files that show the accuracy of our model. A resume of our entire work over the course of the internship can be found at FinalReport.pdf.
 
 ## Authors
 
 [Francisco Andrade](https://github.com/francis-andrade)
 
 [Pedro Silva](https://github.com/Peteraya)
  
