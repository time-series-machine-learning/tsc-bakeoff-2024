# Bake off redux: a review and experimental evaluation of recent time series classification algorithms

Code and results for the paper "Bake off redux: a review and experimental evaluation of
recent time series classification algorithms" published in Data Mining and Knowledge
Discovery, which evaluates 40 time series classification algorithms on 112 UCR
datasets and 30 new datasets.

The paper is open access and available from
[Springer](https://doi.org/10.1007/s10618-024-01022-1). A
[correction](https://doi.org/10.1007/s10618-024-01040-z) gives the corrected values for
Tables 1 and 23 on the Covid3Month_disc, FloodModeling1_disc, FloodModeling2_disc and
FloodModeling3_disc datasets.

## Contents

| Path | Description |
|---|---|
| [results/distance](results/distance) | Distance based classifiers, Section 4.1 (Table 2, Figure 7) |
| [results/feature](results/feature) | Feature based classifiers, Section 4.2 (Table 3, Figure 10) |
| [results/interval](results/interval) | Interval based classifiers, Section 4.3 (Table 4, Figures 14 and 15) |
| [results/shapelet](results/shapelet) | Shapelet based classifiers, Section 4.4 (Table 6, Figures 18 and 19) |
| [results/dictionary](results/dictionary) | Dictionary based classifiers, Section 4.5 (Table 8, Figures 24 and 25) |
| [results/convolution](results/convolution) | Convolution based classifiers, Section 4.6 (Table 10, Figures 28 and 29) |
| [results/deeplearning](results/deeplearning) | Deep learning classifiers, Section 4.7 (Table 12, Figure 33) |
| [results/hybrid](results/hybrid) | Hybrid classifiers, Section 4.8 (Table 13, Figures 37 and 38) |
| [results/best](results/best) | The best classifier from each category and PF on all 142 datasets, Section 5 (Figures 41, 42, 47 and 48, Tables 15 to 18) |
| [results/table_23.csv](results/table_23.csv) | Accuracy on the 30 new datasets for Table 23, with the corrected values |
| [set_bakeoff_classifier.py](set_bakeoff_classifier.py) | The estimator configurations used in the experiments |
| [run_experiments.py](run_experiments.py) | Script to run a single experiment |
| [tsc_bakeoff_2023.ipynb](tsc_bakeoff_2023.ipynb) | Example of using the classifiers directly |
| [static_publication_reqs.txt](static_publication_reqs.txt) | Dependency versions used at the time of publication |

The category folders hold results on the 112 UCR datasets. Together they are used for
Table 14 and Figures 39, 43 and 46. Each results file is named
`<classifier>_<metric>.csv`, where the metric is accuracy, balanced accuracy (`balacc`),
AUROC or negative log likelihood (`logloss`), and has one row per dataset and one
column per resample. `MR` is MultiROCKET, and `WEASEL-1` and `WEASEL-2` are WEASEL v1.0
and v2.0.

## Datasets

The 112 UCR datasets are from the
[UCR Time Series Classification Archive 2018](https://doi.org/10.5281/zenodo.11198697).

The 30 new datasets are available on Zenodo as the
[Time Series Classification Bakeoff Redux Datasets 2024](https://doi.org/10.5281/zenodo.11206358)
and from
[Google Drive](https://drive.google.com/file/d/1vuh6mgNrNKjHr9MMRQP0J0_gGA4dE7E3/view?usp=sharing).
More information on the datasets is available at
[timeseriesclassification.com](http://www.timeseriesclassification.com).

## Running the experiments

There are two ways to run the code: with the latest versions, or with the versions
recorded at the time of publication. Results from the latest versions may differ from
the published results files, as the algorithms have changed since publication.

### Latest versions

Clone this repository and install the latest `tsml-eval` with all optional estimator
dependencies:

    pip install -r requirements.txt

This is the same as:

    pip install tsml-eval[all_extras,deep_learning]

Not all estimator dependencies are installed by default with `pip install tsml-eval`.
For a smaller install, you can install these individually as required.

Run [run_experiments.py](run_experiments.py) from the repository root with the
following arguments:

1. Path to the data directory
2. Path to the results directory
3. The name of the model to run (see
   [set_bakeoff_classifier.py](set_bakeoff_classifier.py), i.e. R-STSF, HC2,
   InceptionTime)
4. The name of the problem to run
5. The resample number to run (0 is base train/test split)

i.e. to run GunPoint using HIVE-COTE V2 on the base train/test split:

    python run_experiments.py data/ results/ HC2 GunPoint 0

Running the script without arguments runs ROCKET on a small example dataset included
with `tsml-eval` and writes to `test_output/`.

The code in this repository was last checked in November 2026 with `tsml-eval` 0.7.0,
`aeon` 1.5.0 and `tsml` 0.10.0 on Python 3.12. It is not actively maintained against
new releases.

### As published

The paper used `tsml-eval` 0.2.1 and `aeon` 0.6.0. `tsml-eval` 0.2.1 contains this
code, so install it with the dependency versions recorded at the time of publication.
This requires Python 3.9 or 3.10. Results from this setup may not match the published
results files exactly.

    pip install -r static_publication_reqs.txt
    pip install --no-deps tsml-eval==0.2.1
    python -m tsml_eval.publications.y2023.tsc_bakeoff.run_experiments data/ results/ HC2 GunPoint 0

The requirements file was generated on Windows, so `pywin32`, `tensorflow-intel`,
`ansicon` and `jinxed` should be removed on other operating systems.

### Exactly reproducing results

To better compare to past results and publications, our results on the 112 UCR datasets
use the randomly generated resamples from the Java
[tsml](https://github.com/time-series-machine-learning/tsml-java) package. To use these
resamples, download the files for each resample into the data directory and add the
`-pr` (predefined resample) argument when running the experiments. These resamples in
.ts file format are available for download here:

<https://drive.google.com/file/d/1V36LSZLAK6FIYRfPx6mmE5euzogcXS83/view?usp=sharing> - 112 UCR datasets using Java tsml resamples

The 30 new datasets use the resampling available by default in the experiments script.
An exception to this is ProximityForest, which is implemented in Java and uses the Java
resampling as a result.

We provide the resample indices used for each dataset for both Java and Python
resamplers here:

Python - <https://drive.google.com/file/d/1aLBP_nhnoqz075puKg30zuF3F_QBOXYM/view?usp=sharing>

Java - <https://drive.google.com/file/d/1FsG7Fp74y_TpaPhJ7U066ot8A07BPhr3/view?usp=sharing>

### Java classifier implementations

Three of the classifiers used in our comparison were implemented in Java due to a lack of
Python implementations which function reliably and are capable of accurately
reproducing published results. These classifiers are the ElasticEnsemble,
ProximityForest and TS-CHIEF. We use the implementations from the Java
[tsml](https://github.com/time-series-machine-learning/tsml-java) package from
revisions where they are available. We make two jar files available for download which
contain the implementations of these classifiers:

<https://drive.google.com/file/d/1oXxpSa5PT9sBuVAbt57TLMANv4TMEejI/view?usp=sharing> - TS-CHIEF and ProximityForest

<https://drive.google.com/file/d/1Vmgg5u7SE2jmsakHVlxPxvT_AfaZ151e/view?usp=sharing> - ElasticEnsemble

These jar files can be run from the command line using the following commands, similar
to the Python classifiers above:

    java -jar tsml-ee.jar -dp=data/ -rp=results/ -cn="FastEE" -dn="ItalyPowerDemand" -f=0

or

    java -jar tsml-forest.jar -dp=data/ -rp=results/ -cn="ProximityForest" -dn="ItalyPowerDemand" -f=0

or

    java -jar tsml-forest.jar -dp=data/ -rp=results/ -cn="TS-CHIEF" -dn="ItalyPowerDemand" -f=0

## Using the classifiers

Most of the classifiers used in the experiments are available in the
[aeon](https://github.com/aeon-toolkit/aeon) Python package, and the others in
[tsml](https://github.com/time-series-machine-learning/tsml-py). They follow the
`scikit-learn` interface. See [tsc_bakeoff_2023.ipynb](tsc_bakeoff_2023.ipynb) for an
example, which can be run online using Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/time-series-machine-learning/tsc-bakeoff-2024/main?filepath=tsc_bakeoff_2023.ipynb)

## Classifier parameters

| Classifier | Parameters |
|---|---|
| 1NN-DTW | Warping window: Full |
| ShapeDTW | Warping window: Full, Subsequence length: 30 |
| EE | Neighbourhood size limit: 0.1, Parameter size limit: 0.5 |
| PF | Number of trees: 100, Number of splits: 5 |
| GRAIL | Classifier: SVM with CV, kernel: SINK, d: max(min(_n_ * 0.4), 100), 3), f: 0.99 |
| Catch22 | Classifier: Random Forest with 500 trees |
| Signatures | Classifier: Random Forest with 500 trees, Truncation depth: 4, Window: dyadic with depth 3 |
| TSFresh | Classifier: Random Forest with 500 trees, Parameter set: efficient, Feature extraction: FRESH |
| FreshPRINCE | Classifier: Rotation Forest with 200 trees, Parameter set: comprehensive |
| RSF | Number of trees: 100, Shapelets per node: 10 |
| STC | n_shapelet_samples: 10000, max_shapelets: min(10 * _n_, 1000) |
| MrSQM | Feature selection strategy: RS, Features per representation: 500, Candidate features per representation: 2000, SAX transformers: 0, SFA Transformers: 5 |
| RDST | Number of shapelets: 10000, Normalization chance: 0.8, Alpha similarity: 0.5 |
| TSF | Number of trees: 500, Intervals per tree: sqrt(m) |
| RISE | Number of trees: 500, ACF lags: 100 |
| CIF | Number of trees: 500, Intervals per tree: sqrt(_m_)*sqrt(_d_), Attributes per tree: 8, Max interval length: _m_/2 |
| DrCIF | Number of trees: 500, Intervals per representation (_rm_=representation length): 4+(sqrt(_rm_)*sqrt(_d_))/3, Attributes per tree: 10, Max interval length: _m_/2 |
| STSF | Number of trees: 500 |
| R-STSF | Classifier: Extra trees with 500 trees, Interval extraction runs: 50 |
| QUANT | Classifier: Extra trees with 200 trees, Interval depth: 6, Quantile divisor: 4 |
| BOSS | Max ensemble size: 500, Accuracy threshold: 0.92 |
| cBOSS | Parameter sets sampled: 250, Max ensemble size: 50 |
| TDE | Parameter sets sampled: 250, Max ensemble size: 50 |
| WEASEL v1.0 | Classifier: Logistic regression, Alphabet size: 4, Feature selection threshold: 0.05 |
| WEASEL v2.0 | Classifier: Logistic regression, Alphabet size: 2, Max feature count: 30000 |
| ROCKET | Classifier: Ridge with cross-validation, Number of kernels: 10000 |
| Arsenal | Ensemble size: 25, Number of kernels: 2000 |
| MultiROCKET | Classifier: Ridge with cross-validation, Number of kernels: 10000 |
| MiniROCKET | Classifier: Ridge with cross-validation, Number of kernels: 10000 |
| Hydra | Classifier: Ridge with cross-validation, Number of groups: 64, Kernels per group: 8 |
| MR-Hydra | Classifier: Ridge with cross-validation, MR kernels: 10000, g: Hydra groups, Hydra kernels per group: 8 |
| CNN | Average pooling size: 3, Batch size: 16, Kernel size: 7, Number of epochs: 2000, Number of layers: 2 |
| ResNet | Batch size: 64, Number of layers: 3, Number of epochs: 1500, n_residual_blocks: 3 |
| InceptionTime | Ensemble size: 5, Batch size: 64, Inception modules: 6, Kernel size: 40, Max pooling size: 3, Number of epochs: 1500, Number of layers: 3, Inception filters: 32 |
| H-InceptionTime | Ensemble size: 5, Batch size: 64, Inception modules: 6, Kernel size: 40, Max pooling size: 3, Number of epochs: 1500, Number of layers: 3, Inception filters: 32 |
| LiteTime | Ensemble size: 5, Batch size: 64, Kernel size: 40, Number of epochs: 1500, Inception filters: 32 |
| TS-CHIEF | Number of trees: 500, EE splitters: 5, RISE splitters: 100, BOSS splitters: 100 |
| HC1 | Alpha: 4 |
| HC2 | Alpha: 4 |
| RIST | Classifier: Extra trees with 500 trees, Number of intervals: sqrt(_m_) * sqrt(_d_) * 15 + 5, Number of shapelets: sqrt(_m_) * 200 + 5 |

## Citation

If you use this work, please cite the paper:

```bibtex
@article{middlehurst2024bake,
  title={Bake off redux: a review and experimental evaluation of recent time series classification algorithms},
  author={Middlehurst, Matthew and Sch{\"a}fer, Patrick and Bagnall, Anthony},
  journal={Data Mining and Knowledge Discovery},
  volume={38},
  number={4},
  pages={1958--2031},
  year={2024},
  publisher={Springer},
  doi={10.1007/s10618-024-01022-1}
}
```

## Contact

For questions about the paper or this repository, contact Matthew Middlehurst at
[m.b.middlehurst@bradford.ac.uk](mailto:m.b.middlehurst@bradford.ac.uk) or on the
[aeon Discord](https://discord.gg/D6rzqHGKRJ) (`matthewmiddlehurst`).
