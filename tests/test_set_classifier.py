"""Tests for publication experiments estimator selection."""

import numpy as np
import pytest
from sklearn.ensemble import RandomForestClassifier
from tsml_eval.testing.testing_utils import _check_set_method, _check_set_method_results

from set_bakeoff_classifier import _set_bakeoff_classifier, bakeoff_classifiers


def test_set_bakeoff_classifier():
    """Test set_bakeoff_classifier method."""
    classifier_list = []
    classifier_dict = {}
    all_classifier_names = []
    _check_set_method(
        _set_bakeoff_classifier,
        bakeoff_classifiers,
        classifier_list,
        classifier_dict,
        all_classifier_names,
    )

    _check_set_method_results(
        classifier_dict,
        estimator_name="Classifiers",
        method_name="_set_bakeoff_classifier",
    )


def test_set_bakeoff_classifier_invalid():
    """Test set_bakeoff_classifier method with invalid estimator."""
    with pytest.raises(ValueError, match="UNKNOWN CLASSIFIER"):
        _set_bakeoff_classifier("invalid")


@pytest.mark.parametrize(
    "name,fast_params",
    [
        ("1NN-DTW", {}),
        ("GRAIL", {}),
        ("Catch22", {"estimator": RandomForestClassifier(n_estimators=5)}),
        ("FreshPRINCE", {"n_estimators": 5, "default_fc_parameters": "minimal"}),
        (
            "TSFresh",
            {
                "estimator": RandomForestClassifier(n_estimators=5),
                "default_fc_parameters": "minimal",
            },
        ),
        ("Signatures", {"estimator": RandomForestClassifier(n_estimators=5)}),
        (
            "STC",
            {
                "estimator": RandomForestClassifier(n_estimators=5),
                "n_shapelet_samples": 50,
                "max_shapelets": 5,
                "batch_size": 10,
            },
        ),
        ("RDST", {"max_shapelets": 10}),
        ("RSF", {"n_estimators": 5}),
        ("MrSQM", {}),
        ("R-STSF", {"n_estimators": 5, "n_intervals": 2}),
        ("RISE", {"n_estimators": 5}),
        ("TSF", {"n_estimators": 5}),
        ("CIF", {"n_estimators": 3, "n_intervals": 2, "att_subsample_size": 2}),
        ("STSF", {"n_estimators": 5}),
        ("DrCIF", {"n_estimators": 3, "n_intervals": 2, "att_subsample_size": 2}),
        ("QUANT", {}),
        ("BOSS", {"max_ensemble_size": 3}),
        ("cBOSS", {"n_parameter_samples": 5, "max_ensemble_size": 3}),
        (
            "TDE",
            {
                "n_parameter_samples": 5,
                "max_ensemble_size": 3,
                "randomly_selected_params": 3,
            },
        ),
        ("WEASEL", {}),
        ("WEASEL-D", {}),
        ("ROCKET", {"n_kernels": 20}),
        ("MiniROCKET", {"n_kernels": 84}),
        ("MultiROCKET", {"n_kernels": 84}),
        ("Arsenal", {"n_kernels": 20, "n_estimators": 2}),
        ("Hydra", {"n_kernels": 2, "n_groups": 4}),
        ("MR-Hydra", {"n_kernels": 2, "n_groups": 4}),
        (
            "HC1",
            {
                "stc_params": {
                    "estimator": RandomForestClassifier(n_estimators=1),
                    "n_shapelet_samples": 5,
                    "max_shapelets": 5,
                    "batch_size": 5,
                },
                "tsf_params": {"n_estimators": 1},
                "rise_params": {"n_estimators": 1},
                "cboss_params": {"n_parameter_samples": 1, "max_ensemble_size": 1},
            },
        ),
        (
            "HC2",
            {
                "stc_params": {
                    "estimator": RandomForestClassifier(n_estimators=1),
                    "n_shapelet_samples": 5,
                    "max_shapelets": 5,
                    "batch_size": 5,
                },
                "drcif_params": {
                    "n_estimators": 1,
                    "n_intervals": 2,
                    "att_subsample_size": 2,
                },
                "arsenal_params": {"n_kernels": 5, "n_estimators": 1},
                "tde_params": {
                    "n_parameter_samples": 1,
                    "max_ensemble_size": 1,
                    "randomly_selected_params": 1,
                },
            },
        ),
        ("RIST", {"n_intervals": 2, "n_shapelets": 5}),
    ],
)
def test_fit_bakeoff_classifiers(name, fast_params):
    """Test fitting and predicting with non-DL bakeoff classifiers."""
    rng = np.random.default_rng(0)
    X = rng.normal(size=(20, 1, 40))
    y = np.array([0, 1] * 10)
    X[y == 1] += 1

    try:
        classifier = _set_bakeoff_classifier(name, random_state=0)
    except ModuleNotFoundError as err:
        pytest.skip(f"Optional dependency not installed: {err}")

    if fast_params:
        classifier.set_params(**fast_params)

    classifier.fit(X, y)
    preds = classifier.predict(X)
    assert preds.shape == (20,)
