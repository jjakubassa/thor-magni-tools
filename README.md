<!--## thor-magni-tools: Tools for Preprocessing and Filtering THÖR-MAGNI Human Motion Dataset-->

<h2 align="center">thor-magni-tools:&thinsp;Tools&thinsp;for&thinsp;Preprocessing&thinsp;and&thinsp;Filtering&thinsp;THÖR&hairsp;&#x0335;&hairsp;MAGNI&thinsp;Human&thinsp;Motion&thinsp;Dataset</h2>

<p align="center">
  <a href="http://thor.oru.se/magni.html"><strong><code>Project Page</code></strong></a>
  <a href="https://arxiv.org/abs/2403.09285"><strong><code>Paper</code></strong></a>
  <a href="https://magni-dash.streamlit.app"><strong><code>Dashboard</code></strong></a>
  <a href="https://zenodo.org/records/10554472"><strong><code>Dataset</code></strong></a>
</p>

<div align='center'>
  <br><img src="doc/MovingPeople.gif" width=70%>
  <br>THÖR-MAGNI provides human gaze data aligned with 6D motion and human-robot interactions.
</div>


## Install

Install [miniconda](http://docs.conda.io/en/latest/miniconda.html). Then, you can install all packages required by running:

```
conda env create -f environment.yml && conda activate thor-magni-tools
```

## Running

### Download the dataset

First, the most important step is to download the dataset from [zenodo](10.5281/zenodo.10407222).
Run:

```
curl -O https://zenodo.org/records/10407223/files/THOR_MAGNI.zip\?download\=1 && unzip -r THOR_MAGNI.zip && rm -rf THOR_MAGNI.zip
```

The CSV files for each Scenario can be found in `THOR_MAGNI\CSVs_Scenarios`.


### CSV headers checker

To check the alignment and consistency of headers in the csv files:

```
python -m thor_magni_tools.run_header_check --dir_path=PATH_TO_SCENARIO_FOLDER --sc_id=Scenario_1
```

### Preprocessing


To preprocess the data with interpolation (and optional downsampling and moving average filter), first one should set the parameters in the [cfg file](https://github.com/tmralmeida/thor-magni-tools/blob/main/thor_magni_tools/preprocessing/cfg.yaml) and then run:

```
python -m thor_magni_tools.run_preprocessing 
```

If [in_path](https://github.com/tmralmeida/thor-magni-tools/blob/main/thor_magni_tools/preprocessing/cfg.yaml#L1) is a folder, it will preprocess the files in the folder in parallel. 
After finishing, the files will be stored in the [pre-specified output path](https://github.com/tmralmeida/thor-magni-tools/blob/main/thor_magni_tools/preprocessing/cfg.yaml#L2) with the 
format | time | frame_id | x | y | z | ag_id | data_label, where `ag_id` is the helmet number and `data_label` is the role of the participant.


### [New Feature] 💥 Synchronization of micro-action labels 💥


```
python -m thor_magni_tools.run_merge_activities --activities_path ../datasets/thor_magni_pub_ready/QTM_frames_activities.csv --files_dir outputs/data/thor_magni/Scenario_3/ --out_path outputs/data/activities/
```

Arguments:
| Parameter                 | Description   |	
| :------------------------ | :-------------|
| `--activities_path` 	          |Raw file with synchronization information from Zenodo |
| `--files_dir` 	    |Preprocessed files or directory of files from `run_preprocessing` |
| `--out_path` 	              | Directory to save the merged files|



### Analysis

```
python -m thor_magni_tools.run_analysis --data_path=DATASET_FOLDER OR DATASET FILE --dataset DATASET_NAME 
```

Such that `DATASET_NAME` in {"thor_magni", "thor", "eth_ucy", "sdd", "atc"}.

Optional Arguments:

| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| `--interpolation` 	        |	None          |used to preprocess the dataset. Max frames without tracking |
| `--average_window` 	        |	None          |used to preprocess the dataset. Number of periods to average |
| `--filtering_markers` 	    |	3D-restoration          |filtering markers type used in THÖR/THÖR-MAGNI tracks |
