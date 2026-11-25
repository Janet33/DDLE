# DDLE: Dataset Density Landscape Evaluation Framework

The code of the paper, **DDLE: Dataset Density Landscape Evaluation**.

This repository contains the Python implementation and experimental setup for the DDLE framework, an internal evaluation framework for density-based clustering results. DDLE assesses clustering quality by comparing the discovered structure against a probability density function (ψ) estimated using Kernel Density Estimation (KDE).

## Framework Overview

The core idea of DDLE is to evaluate how well clusters and outliers align with the modes and valleys of the estimated density landscape of the entire dataset. It provides:

- Density-focused metrics for:
  - Intra-cluster density cohesion (relative to ψ)
  - Inter-cluster density separation (density in the valleys of ψ)
  - Outlier characteristics (density of outliers relative to ψ)
- Z-score normalization based on the dataset's overall density distribution.
- The **Dataset Density Structure Index (DDSI)**, which combines normalized cluster density and separation.

## Repository Structure

1. `ddle_framework.py`: Main DDLE implementation and experiment script.
2. `dbcv.py`: DBCV clustering validation metric.
3. `diagnostics.py`: Optional ARI, NMI, and clustering coverage metrics using available ground-truth labels (not used to compute DDSI).
4. `datasets/`: Dataset files:
   - `Aggregation.txt`
   - `R15.txt`
   - `seeds_dataset.txt`
   - `brca.csv`
   - `glass.csv`
   - `Wine-qt.csv`
5. `tests/test_ddle.py`: Basic checks for DDLE metrics and diagnostics.
6. `requirements.txt`: Python dependencies.
7. `README.md`: Project overview and instructions.

The Moons dataset is generated directly by the script. The included dataset files have been validated against the expected dataset sizes.

## Installation

Use **Python 3.11 or 3.12** and open the repository folder in terminal.

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate it:

   **Windows PowerShell:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

In VS Code, select the `.venv` Python interpreter if it is not selected automatically.

## Running the Experiments

From the repository root, run:

```bash
python ddle_framework.py
```

This runs the **full parameter grids** for all seven datasets, with DBCV, 2D plots, and the final metric demonstration enabled. Full experiments, especially DBCV calculations, may take considerable time.

For a faster exploratory check:

```bash
python ddle_framework.py --datasets Seeds --quick --skip-dbcv --skip-plots --skip-demo --seed 42
```

To run selected datasets using the full parameter grids:

```bash
python ddle_framework.py --datasets Moons R15 --seed 42
```

The script will:

- Load the datasets and check their expected sizes.
- Tune DBSCAN, OPTICS, and MeanShift using Silhouette score.
- Evaluate the clustering results using DDLE metrics and standard validation indices under four KDE configurations.
- Report available ARI, NMI, and clustering coverage diagnostics.
- Save CSV results and 2D clustering plots (unless plotting is skipped).
- Print progress updates and summary analyses.

**Note:** `--quick` reduces the hyperparameter search grid and is intended for testing, not reproducing the paper results. `--skip-dbcv` leaves the DBCV output as `NaN`. The `--seed` option controls random sampling of inter-cluster path endpoints; it does not seed every randomized stage of bandwidth estimation or model selection. The optimized script reuses KDE-independent tuning across KDE configurations. Results may differ from earlier experiments due to settings, software versions, or random sampling.

## Output

- **Console:** Progress updates, metrics, and summary tables.
- **`results/` directory:**
  - CSV files: `[DatasetName]_[KDE_ConfigName]_evaluation_primary_tuned.csv`.
  - PNG files: `[DatasetName]_[Algorithm]_Psi_[KDE_ConfigName]_tuned_plot.png` (for 2D datasets).

The `results/` folder is created automatically.

## Tests

```bash
python -m pytest -q
```
