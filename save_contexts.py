import gzip
import io
import os
from sqlitedict import SqliteDict
import pickle
import json

# list directories in the data folder
dataset_names = os.listdir("data")
dataset_names = [name for name in dataset_names if os.path.isdir(f"data/{name}")]

# mkdir dotfiles
if not os.path.exists("dotfiles"):
    os.mkdir("dotfiles")

VISIBLE_DATABASES = {
    "sae-features_lin-effects_final-1-pos_nsamples8192_nctx64": "SAE Features Linear Effects Final 1 Position",
    # "sae-features_lin-effects_final-1-pos_nsamples8192_nctx64": "SAE Features Linear Effects Final 5 Positions",
    "sae-features_lin-effects_sum-over-pos_nsamples8192_nctx64": "SAE Features Linear Effects Sum Over Position",
    # "sae-features_activations_final-1-pos_nsampdf les8192_nctx64": "SAE Features Activations Final 1 Position",
    "sae-features_activations_final-5-pos_nsamples8192_nctx64": "SAE Features Activations Final 5 Positions",
    "sae-features_activations_sum-over-pos_nsamples8192_nctx64": "SAE Features Activations Sum Over Position",
    "parameter-gradient-projections": "Parameter Gradient Projections",
}

for name in VISIBLE_DATABASES.keys():
    print(name)
    if not os.path.exists(f"dotfiles/{name}"):
        os.mkdir(f"dotfiles/{name}")
    with SqliteDict(f"data/{name}/database.sqlite") as db:
        for cluster_idx, compressed_bytes in db.items():
            decompressed_object = io.BytesIO(compressed_bytes)
            with gzip.GzipFile(fileobj=decompressed_object, mode='rb') as file:
                cluster_data = pickle.load(file)
            cluster_contexts = cluster_data["contexts"]
            with open(f"dotfiles/{name}/{cluster_idx}.json", "w") as f:
                f.write(json.dumps(cluster_contexts))