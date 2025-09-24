# Ontology-Corpus-Comparison Topic Discovery

The methodology measures the semantic similarities between topics in a set of ontologies and sections (referred to as segments) of the corpus of national constitutions.

Topics that are similar to a given segment are regarded as coding the meaning of the segment. If the set of topics similar to a segment belong to more than one ontology, then the ontologies are aligned conceptually and we have discovered a conceptual mapping between ontologies.

## System Requirements

- **Operating Systems**: macOS (Intel or ARM), Linux, or Windows
- **RAM**: Minimum 8GB recommended, 16GB+ for large datasets
- **Storage**: At least 5GB of free space
- **Python**: Version 3.9.21 (managed via Anaconda)

## Quick Start

1. Install [Anaconda](https://www.anaconda.com/download)
2. Open a new terminal window and run:
   ```
   conda create -n occ python=3.9.21 pip jupyter
   conda activate sat
   ```
3. Clone or download this repository
4. Navigate to the repository directory and install required packages:
   ```
   pip install "pip<24.1"
   pip install -r required_packages.txt
   ```
5. Launch Jupyter Notebook:
   ```
   jupyter notebook
   ```
6. Open `installer.ipynb` and select **"Run All Cells"** from the "Run" tab

---

## Detailed Installation Instructions

### Step 1: Download and Install Anaconda

- Download and install [Anaconda](https://www.anaconda.com/download)
- Accept the default installation settings
- Choose to initialize Conda when prompted during installation

### Step 2: Create Conda Environment

After installation, open a new terminal window (Command Prompt or PowerShell on Windows, Terminal on macOS/Linux) and create the environment:

```
conda create -n occ python=3.9.21 pip jupyter
conda activate occ
```

### Step 3: Obtain the Repository

The recommended method is to use GitHub Desktop to clone the repository, but you can also download it as a ZIP file.

The repository includes:

- `analysis/`: Jupyter notebook (`sat_expansion_pipeline.ipynb`.), `_library` folder with Python code, and `outputs/` folder with paper results
- `cython/`: Prebuilt shared objects (`angular_distance.so`) for Mac Intel, Mac ARM, and Linux Intel
- `installer.ipynb`: Jupyter notebook for installing data and NLP model resources
- `processing/`: Python code for building the CCP data model
- `required_packages.txt`: Required Python packages for your Conda environment
- `README.md`: This file

### Step 4: Install Required Packages

Navigate to the repository directory in your terminal. For example:

```
cd "/Users/janedoe/Downloads/SAT-method-main"
```

Then install the required packages:

```
pip install -r required_packages.txt
```

### Step 5: Launch Jupyter Notebook

With the `occ` environment activated, run:

```
jupyter notebook
```

This will open a new browser tab with the Jupyter interface.

### Step 6: Run the Installer

Using Jupyter, navigate to the repository folder and open `installer.ipynb`. Select **"Run All Cells"** from the "Run" menu.

This will populate your top-level directory with:

- `data/`: Constitutions and ontology required to build the CCP data mode. A precompiled copy of the CCP data model is also downloaded (see below). 
- `model/`: Serialized objects from text and topic processing
- `use_ml_3/`: Multilingual sentence-level encoder

Depending on your machine and internet connection, this may take several minutes.

---

## Platform-Specific Step: Configure `angular_distance.so`

The `processing/` directory includes `angular_distance.so` compiled for Mac Intel by default.

### Pre-compiled versions

If you're using one of these platforms, copy the appropriate file from the `cython/` subdirectories:
- Mac Intel: `cython/mac_intel/angular_distance.so`
- Mac ARM (M1/M2): `cython/mac_arm/angular_distance.so`
- Linux Intel: `cython/linux_intel/angular_distance.so`

Paste the file in the `analysis/_library` and `processing/`, replacing the existing files.

### Building your own version

If you're on a different architecture, build your own shared object file:

1. Navigate to the `cython/` folder
2. Run:
   ```
   conda install cython
   python setup.py build_ext --inplace
   ```
3. Rename the generated file (e.g., `angular_distance.cpython-39-darwin.so`) to `angular_distance.so`
4. Move the file to `analysis/_library` and `processing/`, replacing the existing files.

Ensure these steps are performed within the activated `sat` environment.

---

## Data Processing

### Running `pipeline.py`

`pipeline.py` processes data sources located in `../data/` and is configured through the `config` data structure in the `main()` function.

Steps:

1. Open a new tab in your terminal and activate the `occ` conda environment
2. Navigate to the `processing/` directory 
3. In `pipeline.py`, set the `run` flag to `True` for any data source you want to process
4. Run the pipeline:
   ```
   python pipeline.py
   ```

The configuration mirrors the `data/` directory layout, so no changes are required beyond updating the `run` flags.

If using a Mac, you may receive the following message:

```
"angular_distance.so" Not Opened: Apple could not verify “angular_distance.so” is free of malware that may harm your Mac or compromise your privacy.
```
To resolve this issue, please see how to build your own version of the file above.

---

## Analysis

Using Jupyter, navigate to the `analysis/` folder and open `relational_analysis.ipynb`.

Run the first cell to complete initialization. Once initialized, you can run other cells as needed to perform specific analyses.

The notebook contains detailed documentation for each analysis step.

---

## Troubleshooting

### Common Issues

1. **"No module named X" error**: Make sure you've installed all required packages and activated the `sat` environment
   ```
   conda activate sat
   pip install -r required_packages.txt
   ```

2. **Shared object/DLL loading issues**: Ensure you're using the correct `angular_distance.so` file for your system architecture

3. **Memory errors**: If you encounter memory errors during processing, try reducing batch sizes in `pipeline.py` or processing smaller subsets of data

4. **Jupyter kernel dies**: Increase the memory limit for your Jupyter kernel or reduce the size of data being processed in a single cell

### Getting Help

If you encounter issues not covered in this documentation, please file an issue on the repository with:
- Your operating system and version
- Python version (`python --version`)
- The complete error message
- Steps to reproduce the issue

---

## License and Citation

### License

This project is licensed under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) license.

For questions or additional information, please contact Roy Gardner (roybowesgardner@gmail.com) or Matthew Martin (mjmartin@utexas.edu).

---

Happy analyzing!
