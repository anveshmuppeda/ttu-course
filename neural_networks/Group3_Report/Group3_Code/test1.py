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

from opendataval.experiment import ExperimentMediator

dataset_name = "adult"
train_count, valid_count, test_count = 1000, 100, 500
noise_rate = 0.2
noise_kwargs = {'noise_rate': noise_rate}
model_name = "sklogreg"
metric_name = "accuracy"

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

data_evaluators = [ 
    DVRL(rl_epochs=20), # Data valuation using Reinforcement Learning
    KNNShapley(k_neighbors=valid_count), # KNN-Shapley
]
exper_med = exper_med.compute_data_values(data_evaluators=data_evaluators)

# Saving the results
output_dir = f"./{dataset_name}_{noise_rate=}/"
exper_med.set_output_directory(output_dir)

# Evaluate noisy detection
exper_med.evaluate(noisy_detection)

# Plotting
fig = plt.figure(figsize=(15, 40))
df, fig = exper_med.plot(discover_corrupted_sample, fig, col=2)
# plt.show()

print(df)