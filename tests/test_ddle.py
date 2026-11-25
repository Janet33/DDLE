import sys
import unittest
from pathlib import Path
import numpy as np
from sklearn.neighbors import KernelDensity

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from diagnostics import external_and_coverage_metrics
from ddle_framework import evaluate_clustering_framework, calculate_dataset_density_stats

class DiagnosticsTests(unittest.TestCase):
    def test_perfect_reference_match(self):
        m = external_and_coverage_metrics(np.array([0, 0, 1, 1]), [4, 4, 9, 9])
        self.assertAlmostEqual(m['ARI_all'], 1.0)
        self.assertAlmostEqual(m['NMI_all'], 1.0)
        self.assertAlmostEqual(m['retained_fraction'], 1.0)
        self.assertEqual(m['cluster_count_diagnostic'], 2)

    def test_noise_and_missing_reference(self):
        m = external_and_coverage_metrics(np.array([0, 0, -1, 1]), None)
        self.assertEqual(m['outlier_fraction'], .25)
        self.assertTrue(np.isnan(m['ARI_all']))

    def test_bad_reference_length_rejected(self):
        with self.assertRaises(ValueError):
            external_and_coverage_metrics([0, 0, 1, 1], [0, 1])

    def test_density_variation_denominator_and_reproducibility(self):
        data = np.array([[-2., 0], [-1.9, 0.2], [-1.8,-0.1],
                         [2.,0], [2.1,0.1], [2.2,-0.1], [7.,8.]])
        labels = np.array([0,0,0,1,1,1,-1])
        est = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(data)
        mu, sd, vals = calculate_dataset_density_stats(data, est)
        a = evaluate_clustering_framework(data, labels, est, mu, sd, vals,
            separation_random_state=123, n_separation_samples=2, n_path_points=10)
        b = evaluate_clustering_framework(data, labels, est, mu, sd, vals,
            separation_random_state=123, n_separation_samples=2, n_path_points=10)
        self.assertEqual(int(a['n_x']), 6)
        expected = np.sqrt(sum(((vals[labels==x]-vals[labels==x].mean())**2).sum()
                               for x in (0,1))/6)
        self.assertAlmostEqual(a['wwC_x_psi'], expected, places=12)
        self.assertEqual(a['Sep(X)'], b['Sep(X)'])
        self.assertAlmostEqual(a['DDSI_x_psi'], a['z_mu_x_psi'] - a['z_Sep(X)'])

if __name__=='__main__':
    unittest.main()
