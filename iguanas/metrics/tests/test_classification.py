import numpy as np
import pandas as pd
import iguanas.metrics as iguanas_metrics
import sklearn.metrics as sklearn_metrics
import pytest


@pytest.fixture
def create_data():
    np.random.seed(0)
    y_pred = np.random.randint(0, 2, 1000)
    y_true = np.random.randint(0, 2, 1000)
    y_preds = pd.DataFrame(np.random.randint(0, 2, size=(1000, 2)))
    weights = y_true * 10
    amts = np.random.uniform(0, 1000, 1000)
    return y_true, y_pred, weights, y_preds, amts


def test_Precision(create_data):
    y_true, y_pred, weights, y_preds, _ = create_data
    precision = iguanas_metrics.Precision()
    for w in [None, weights]:
        prec_calc = precision.fit(y_pred, y_true, w)
        prec_exp = sklearn_metrics.precision_score(
            y_true, y_pred, sample_weight=w)
        assert prec_calc == prec_exp
    for w in [None, weights]:
        prec_calc = precision.fit(y_preds, y_true, w)
        for i, col in enumerate(y_preds.columns):
            prec_exp = sklearn_metrics.precision_score(
                y_true, y_preds[col], sample_weight=w)
            assert prec_calc[i] == prec_exp


def test_Recall(create_data):
    y_true, y_pred, weights, y_preds, _ = create_data
    recall = iguanas_metrics.Recall()
    for w in [None, weights]:
        recall_calc = recall.fit(y_pred, y_true, w)
        recall_exp = sklearn_metrics.recall_score(
            y_true, y_pred, sample_weight=w)
        assert recall_calc == recall_exp
    for w in [None, weights]:
        recall_calc = recall.fit(y_preds, y_true, w)
        for i, col in enumerate(y_preds.columns):
            recall_exp = sklearn_metrics.recall_score(
                y_true, y_preds[col], sample_weight=w)
            assert recall_calc[i] == recall_exp


def test_FScore(create_data):
    y_true, y_pred, weights, y_preds, _ = create_data
    f1 = iguanas_metrics.FScore(1)
    for w in [None, weights]:
        f1_calc = f1.fit(y_pred, y_true, w)
        f1_exp = sklearn_metrics.fbeta_score(
            y_true, y_pred, beta=1, sample_weight=w)
        assert f1_calc == f1_exp
    for w in [None, weights]:
        f1_calc = f1.fit(y_preds, y_true, w)
        for i, col in enumerate(y_preds.columns):
            f1_exp = sklearn_metrics.fbeta_score(
                y_true, y_preds[col], sample_weight=w, beta=1)
            assert f1_calc[i] == f1_exp


def test_repr():
    p = iguanas_metrics.Precision()
    r = iguanas_metrics.Recall()
    f1 = iguanas_metrics.FScore(1)
    rev = iguanas_metrics.Revenue(y_type='Fraud', chargeback_multiplier=2)
    assert 'Precision' == p.__repr__()
    assert 'Recall' == r.__repr__()
    assert 'FScore with beta=1' == f1.__repr__()
    assert 'Revenue with y_type=Fraud, chargeback_multiplier=2' == rev.__repr__()


def test_Revenue(create_data):
    y_true, y_pred, _, y_preds, amts = create_data
    r = iguanas_metrics.Revenue(y_type='Fraud', chargeback_multiplier=2)
    rev_calc = r.fit(y_pred, y_true, amts)
    rev_exp = 15085.412726571973
    assert rev_calc == rev_exp
    rev_calc = r.fit(y_preds, y_true, amts)
    rev_exp = np.array([-10492,  55162])
    assert all(rev_calc == rev_exp)
    r = iguanas_metrics.Revenue(y_type='NonFraud', chargeback_multiplier=2)
    rev_calc = r.fit(y_pred, y_true, amts)
    rev_exp = 19750.05877204858
    assert rev_calc == rev_exp
    rev_calc = r.fit(y_preds, y_true, amts)
    rev_exp = np.array([-29783,  44867])
    assert all(rev_calc == rev_exp)


def test_warnings_Precision(create_data):
    y_true, y_pred, _, _, _ = create_data
    precision = iguanas_metrics.Precision()
    with pytest.raises(TypeError, match="`y_true` must be a numpy.ndarray or pandas.core.series.Series or databricks.koalas.series.Series. Current type is list."):
        precision.fit(y_true, [])
    with pytest.raises(TypeError, match="`y_preds` must be a numpy.ndarray or pandas.core.series.Series or pandas.core.frame.DataFrame or databricks.koalas.series.Series or databricks.koalas.frame.DataFrame. Current type is list."):
        precision.fit([], y_pred)
    with pytest.raises(TypeError, match="`sample_weight` must be a numpy.ndarray or pandas.core.series.Series or databricks.koalas.series.Series. Current type is list."):
        precision.fit(y_true, y_pred, [])


def test_warnings_Recall(create_data):
    y_true, y_pred, _, _, _ = create_data
    recall = iguanas_metrics.Recall()
    with pytest.raises(TypeError, match="`y_true` must be a numpy.ndarray or pandas.core.series.Series or databricks.koalas.series.Series. Current type is list."):
        recall.fit(y_true, [])
    with pytest.raises(TypeError, match="`y_preds` must be a numpy.ndarray or pandas.core.series.Series or pandas.core.frame.DataFrame or databricks.koalas.series.Series or databricks.koalas.frame.DataFrame. Current type is list."):
        recall.fit([], y_pred)
    with pytest.raises(TypeError, match="`sample_weight` must be a numpy.ndarray or pandas.core.series.Series or databricks.koalas.series.Series. Current type is list."):
        recall.fit(y_true, y_pred, [])


def test_warnings_FScore(create_data):
    y_true, y_pred, _, _, _ = create_data
    fs = iguanas_metrics.FScore(1)
    with pytest.raises(TypeError, match="`y_true` must be a numpy.ndarray or pandas.core.series.Series or databricks.koalas.series.Series. Current type is list."):
        fs.fit(y_true, [])
    with pytest.raises(TypeError, match="`y_preds` must be a numpy.ndarray or pandas.core.series.Series or pandas.core.frame.DataFrame or databricks.koalas.series.Series or databricks.koalas.frame.DataFrame. Current type is list."):
        fs.fit([], y_pred)
    with pytest.raises(TypeError, match="`sample_weight` must be a numpy.ndarray or pandas.core.series.Series or databricks.koalas.series.Series. Current type is list."):
        fs.fit(y_true, y_pred, [])


def test_warnings_Revenue(create_data):
    y_true, y_pred, weights, _, _ = create_data
    r = iguanas_metrics.Revenue(y_type='Fraud', chargeback_multiplier=2)
    with pytest.raises(TypeError, match="`y_true` must be a numpy.ndarray or pandas.core.series.Series or databricks.koalas.series.Series. Current type is list."):
        r.fit(y_true, [], weights)
    with pytest.raises(TypeError, match="`y_preds` must be a numpy.ndarray or pandas.core.series.Series or pandas.core.frame.DataFrame or databricks.koalas.series.Series or databricks.koalas.frame.DataFrame. Current type is list."):
        r.fit([], y_pred, weights)
    with pytest.raises(TypeError, match="`sample_weight` must be a numpy.ndarray or pandas.core.series.Series or databricks.koalas.series.Series. Current type is list."):
        r.fit(y_true, y_pred, [])
    with pytest.raises(ValueError, match='`y_type` must be either "Fraud" or "NonFraud"'):
        iguanas_metrics.Revenue(y_type='Wrong', chargeback_multiplier=2)
