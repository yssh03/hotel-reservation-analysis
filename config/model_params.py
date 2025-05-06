from scipy.stats import randint, uniform

LIGHTGM_PARAMS = {
    "n_estimators": randint(100, 500),
    "max_depth": randint(5, 50),
    "learning_rate": uniform(0.01, 0.2),
    "num_leaves": randint(20, 100),
    "boosting_type": ["gbdt", "dart", "goss"]
}

RANDOM_SEARCH_PARAMS = {
    "verbose": 2,
    "n_iter": 5,
    "cv": 2,
    "random_state": 36,
    "scoring": "accuracy",
    "n_jobs": -1
}
