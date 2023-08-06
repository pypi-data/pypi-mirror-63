
<!-- README.md is generated from README.Rmd. Please edit that file -->

# ncaa-march-madness-2020

<!-- badges: start -->

<!-- badges: end -->

The goal of ncaa-march-madness-2020 is to store the notebooks for this
[Kaggle
Competition](https://www.kaggle.com/c/google-cloud-ncaa-march-madness-2020-division-1-mens-tournament/overview),
see
[GitBook](https://jiaxiangbu.github.io/ncaa-march-madness-2020/cookbook.html)
including

  - Baseline
  - XGBOOST 
  - Target encoding
  - ID embedding
  - GBDT + LR
  - GBDT + LR k-fold
  - 
  - Linear vs. Tree linear?
  - Auto-encoder 
  - Python 

## How to use

All notebooks work in the `analysis` directory, and save all data files
in `input`, `output` and `data` directories.

``` r
fs::dir_tree("analysis", recurse = TRUE, regexp = "ipynb")
#> analysis
#> +-- baseline.ipynb
#> +-- evaluate-features.ipynb
#> +-- gbdt_lr.ipynb
#> +-- gbdt_lr_CV.ipynb
#> +-- id2vec.ipynb
#> +-- linear-base-learner.ipynb
#> +-- march-madness-2020-ncaam-simple-lightgbm-on-kfold.ipynb
#> +-- Obtain_Answer.ipynb
#> +-- outliers.ipynb
#> +-- params_tuning.ipynb
#> +-- paris-madness.ipynb
#> +-- pkg_test.ipynb
#> \-- target-encoding.ipynb
fs::dir_tree(recurse = TRUE, regexp = "input|output|data")
#> .
#> +-- data
#> |   +-- feature_importances.csv
#> |   +-- id2vec.npy
#> |   +-- NCAA2020_Kenpom.csv
#> |   +-- outlier_df.csv
#> |   +-- submission_True.csv
#> |   +-- team_strength_embedding.csv
#> |   +-- Tourney_Reuslt.csv
#> |   \-- Tourney_Reuslt_inputs.csv
#> +-- input
#> |   +-- google-cloud-ncaa-march-madness-2020-division-1-mens-tournament
#> |   |   +-- MDataFiles_Stage1
#> |   |   |   +-- Cities.csv
#> |   |   |   +-- Conferences.csv
#> |   |   |   +-- MConferenceTourneyGames.csv
#> |   |   |   +-- MGameCities.csv
#> |   |   |   +-- MMasseyOrdinals.csv
#> |   |   |   +-- MNCAATourneyCompactResults.csv
#> |   |   |   +-- MNCAATourneyDetailedResults.csv
#> |   |   |   +-- MNCAATourneySeedRoundSlots.csv
#> |   |   |   +-- MNCAATourneySeeds.csv
#> |   |   |   +-- MNCAATourneySlots.csv
#> |   |   |   +-- MRegularSeasonCompactResults.csv
#> |   |   |   +-- MRegularSeasonDetailedResults.csv
#> |   |   |   +-- MSeasons.csv
#> |   |   |   +-- MSecondaryTourneyCompactResults.csv
#> |   |   |   +-- MSecondaryTourneyTeams.csv
#> |   |   |   +-- MTeamCoaches.csv
#> |   |   |   +-- MTeamConferences.csv
#> |   |   |   +-- MTeams.csv
#> |   |   |   \-- MTeamSpellings.csv
#> |   |   +-- MEvents2015.csv
#> |   |   +-- MEvents2016.csv
#> |   |   +-- MEvents2017.csv
#> |   |   +-- MEvents2018.csv
#> |   |   +-- MEvents2019.csv
#> |   |   +-- MPlayers.csv
#> |   |   \-- MSampleSubmissionStage1_2020.csv
#> |   \-- google-cloud-ncaa-march-madness-2020-division-1-mens-tournament.zip
#> +-- large_data
#> \-- output
#>     \-- paris-submission.csv
```

## Download Data

From <https://github.com/Kaggle/kaggle-api>

``` bash
kaggle competitions download -c google-cloud-ncaa-march-madness-2020-division-1-mens-tournament -p input
mkdir input/google-cloud-ncaa-march-madness-2020-division-1-mens-tournament
unzip input/google-cloud-ncaa-march-madness-2020-division-1-mens-tournament.zip -d input/google-cloud-ncaa-march-madness-2020-division-1-mens-tournament
```

<h4 align="center">

**Code of Conduct**

</h4>

<h6 align="center">

Please note that the `ncaa-march-madness-2020` project is released with
a [Contributor Code of
Conduct](https://github.com/JiaxiangBU/ncaa-march-madness-2020/blob/master/CODE_OF_CONDUCT.md).<br>By
contributing to this project, you agree to abide by its terms.

</h6>

<h4 align="center">

**License**

</h4>

<h6 align="center">

What license it uses © [Jiaxiang Li;Jiatao Li;Zhipeng Liang;Yue
Pan](https://github.com/JiaxiangBU/ncaa-march-madness-2020/blob/master/LICENSE.md)

</h6>
