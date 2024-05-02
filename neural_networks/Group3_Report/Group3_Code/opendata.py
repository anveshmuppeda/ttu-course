# Imports
import numpy as np
import pandas as pd

# Opendataval
from opendataval.dataloader import Register, DataFetcher, mix_labels, add_gauss_noise
from opendataval.dataval import (
    AME,
    DVRL,
    BetaShapley,
    DataBanzhaf,
    DataOob,
    DataShapley,
    InfluenceSubsample,
    KNNShapley,
    LavaEvaluator,
    LeaveOneOut,
    RandomEvaluator
)
from opendataval.experiment.exper_methods import (
    discover_corrupted_sample,
    noisy_detection,
    remove_high_low,
    increasing_bin_removal,
    save_dataval
)
from matplotlib import pyplot as plt

# Importing ExperimentMediator from opendataval.experiment module
from opendataval.experiment import ExperimentMediator

# Defining dataset parameters
dataset_name = "adult"
train_count, valid_count, test_count = 1000, 100, 500
noise_rate = 0.2
noise_kwargs = {'noise_rate': noise_rate}
model_name = "sklogreg"
metric_name = "accuracy"

# Setting up ExperimentMediator object with dataset and model details
exper_med = ExperimentMediator.model_factory_setup(
    dataset_name=dataset_name,
    cache_dir="../data_files/",  
    force_download=False,
    train_count=train_count,
    valid_count=valid_count,
    test_count=test_count,
    add_noise=mix_labels, 
    noise_kwargs=noise_kwargs,
    train_kwargs={},
    model_name=model_name,
    metric_name=metric_name
)

# Defining data evaluators (algorithms) to compute data values
data_evaluators = [ 
    RandomEvaluator()
    # List of other algorithms to be evaluated, commented out for now
]

# Computing data values using ExperimentMediator
exper_med = exper_med.compute_data_values(data_evaluators=data_evaluators)

# Setting the output directory for saving results
output_dir = f"./{dataset_name}_{noise_rate=}/"
exper_med.set_output_directory(output_dir)

# Running the noisy detection experiment and saving the output
exper_med.evaluate(noisy_detection, save_output=True)

# Plotting the results of the experiment to discover corrupted samples
fig = plt.figure(figsize=(15, 40))
df, fig = exper_med.plot(discover_corrupted_sample, fig, col=2, save_output=True)
plt.show()

# Plotting the results of the remove_high_low experiment and saving the output
fig = plt.figure(figsize=(15, 40))
df_resp, fig = exper_med.plot(remove_high_low, fig, col=2, save_output=True)
plt.show()
