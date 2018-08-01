# INESCTEC-FLYINGNETWORKS



We have done 2 different scripts that should be run:

- build_model.py: used to build the model. After the model is built, 3 .json files are saved at DataSet/Models-json with the 3 models corresponding to Throughput, Delay and Pdr, and 3 .hdf5 files are saved at DataSet/Checkpoints with the corresponding weights. After that, you should put these files in the DataSet folder, and change their name to model_<QUALITY_METRIC>.json and model_<QUALITY_METRIC>.hdf5 for each corresponding file.
Ps: in the case of the hdf5 files, everytime this script runs, it generates the 3 files with names like "checkpoint<NUMBER>", so just use the 3 highest numbered files for the last model generated, being the small numbered the Throughput file and the bigger the Pdr. 

- best_topology.py: used to get the best topology for all the 10 scenarios. After the script is over, it generates 10 .json files named Fmaps-Topology-<NUMBER>.json that has the position of the 3 UAVs and the corresponding 10 .csv files named Fmaps-Topology-<NUMBER>-Qualities.csv with the Throughput, Delay and Pdr corresponding to that topology in that scenario. All these files are saved at DataSet/Topologies-json. After that, we can use the .json files for simulation in Ns-3. 
  
  All code was done considering python3 and it is placed at the src folder. We also have a FinalResults folder, where we some plots and some excel analysing the data obtained. All of our work during this one month internship can be resumed with the presention present at FinalResults folder, also.  
