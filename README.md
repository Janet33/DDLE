# DDLE: Dataset Density Landscape Evaluation Framework

The code of the paper, DDLE: Dataset Density Landscape Evaluation

This repository contains the Python implementation and experimental setup for the DDLE framework, a novel internal evaluation framework for density-based clustering results. DDLE assesses clustering quality by comparing the discovered structure against an explicit, probability density function (ψ) derived using Kernel Density Estimation (KDE).

## Framework Overview

The core idea of DDLE is to evaluate how well clusters and outliers align with the modes and valleys of the estimated density landscape of the entire dataset. It provides:

- A suite of intrinsically density-focused metrics quantifying:
    - Intra-cluster density cohesion (relative to ψ)
    - Inter-cluster density separation (density in "valleys" of ψ)
    - Outlier characteristics (density of outliers relative to ψ)
- Z-score normalization of these metrics based on the dataset's overall density distribution for standardized and interpretable scores.
- The Dataset Density Structure Index (DDSI_x,ψ), a composite index balancing cluster density and separation clarity.

## Repository Structure

1.  `ddle_framework.py`: The main Python script containing the DDLE implementation and experiment execution logic.
2.  `DBCV.py`: The Python file containing the DBCV metric implementation (as it's a dependency).
3.  `datasets/` directory (with dataset files):
    - Aggregation.txt
    - R15.txt
    - seeds_dataset.txt
    - brca.csv
    - glass.csv
    - Wine-qt.csv
4.  `README.md`: Provides an overview of the research and code structure.
5.  `requirements.txt`: All Python package dependencies and their versions used.
    
## Installation

1. Install the required packages. `requirements.txt` has been provided:
    ```bash
    pip install -r requirements.txt
    ```
    Otherwise, install them manually:
    ```bash
    pip install numpy pandas scikit-learn scipy matplotlib seaborn
    ```

## Running the Experiments

1.  Ensure all dataset files are present in the `datasets/` directory and that `DBCV.py` is in the same directory as `ddle_framework.py`.
2.  Execute the main script from the root directory of the cloned repository:
    ```bash
    python ddle_framework.py
    ```
3.  The script will:
    *   Load each dataset.
    *   Perform hyperparameter tuning for DBSCAN, OPTICS, and MeanShift using Silhouette score.
    *   Run clustering with the best-tuned parameters.
    *   Evaluate results using DLADE metrics and baseline internal validation indices for four different KDE configurations.
    *   Save detailed results (metrics) as CSV files and clustering plots (for 2D data) as PNG files into the `results/dlade_results_7datasets/` directory.
    *   Print summary analyses and a demonstration of DDLE metrics to the console.

## Output

-   **Console Output:** Progress updates, summary tables, and demo section printouts.
-   **`results/ddle_results_7datasets/` directory:**
    -   CSV files: `[DatasetName]_[KDE_ConfigName]_evaluation_primary_tuned.csv` containing detailed metrics for each algorithm run.
    -   PNG files: `[DatasetName]_[AlgoName]_Psi_[KDE_ConfigName]_tuned_plot.png` visualizing 2D clustering results with KDE contours.

