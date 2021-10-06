### Setup

1.  Set up environment

        > conda env create -f environment.yml

2.  Activate env:

        > conda activate nyc_airbnb_dev

### Commands

Delete all mlflow envs:

      for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda uninstall --name $e --all -y;done
