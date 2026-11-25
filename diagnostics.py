"""read-only external DDLE diagnostics (not part of DDSI).

Ground-truth labels are used ONLY after clustering, not in KDE or parameter tuning.
Noise is treated as an additional predicted label for ARI_all/NMI_all.
Retained-only ARI/NMI exclude predicted noise; comparisons are conditional on
which points each algorithm retained and should not be compared in isolation.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score


def external_and_coverage_metrics(labels, reference_labels=None):
    """Return ground-truth agreement when available, and coverage diagnostics always.

    Output is a flat dict for inclusion in experiment CSVs.
    Undefined entries are np.nan, never fabricated numbers.
    """
    pred = np.asarray(labels).reshape(-1)
    n = pred.size
    if n == 0:
        raise ValueError('labels must contain at least one observation')
    assigned = pred != -1
    result = {
        'retained_fraction': float(assigned.mean()),
        'outlier_fraction': float((~assigned).mean()),
        'cluster_count_diagnostic': int(np.unique(pred[assigned]).size),
        'ARI_all': np.nan, 'NMI_all': np.nan,
        'ARI_retained': np.nan, 'NMI_retained': np.nan,
        'reference_label_count': np.nan,
    }
    if reference_labels is None:
        return result
    true = np.asarray(reference_labels).reshape(-1)
    if true.size != n:
        raise ValueError('reference label length differs from prediction length')
    known = np.asarray(~pd.isna(true), dtype=bool)
    if not known.any():
        return result
    result['reference_label_count'] = int(np.unique(true[known]).size)
    result['ARI_all'] = float(adjusted_rand_score(true[known], pred[known]))
    result['NMI_all'] = float(normalized_mutual_info_score(true[known], pred[known]))
    mask = known & assigned
    if mask.sum() >= 2:
        result['ARI_retained'] = float(adjusted_rand_score(true[mask], pred[mask]))
        result['NMI_retained'] = float(normalized_mutual_info_score(true[mask], pred[mask]))
    return result
