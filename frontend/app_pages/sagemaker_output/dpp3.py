from sagemaker_sklearn_extension.decomposition import RobustPCA
from sagemaker_sklearn_extension.externals import Header
from sagemaker_sklearn_extension.impute import RobustImputer
from sagemaker_sklearn_extension.impute import RobustMissingIndicator
from sagemaker_sklearn_extension.preprocessing import NALabelEncoder
from sagemaker_sklearn_extension.preprocessing import QuantileExtremeValuesTransformer
from sagemaker_sklearn_extension.preprocessing import RobustStandardScaler
from sagemaker_sklearn_extension.preprocessing import ThresholdOneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline

# Given a list of column names and target column name, Header can return the index
# for given column name
HEADER = Header(
    column_names=[
        'MEDV', 'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD',
        'TAX', 'PTRATIO', 'B', 'LSTAT'
    ],
    target_column_name='MEDV'
)


def build_feature_transform():
    """ Returns the model definition representing feature processing."""

    # These features can be parsed as numeric.

    numeric = HEADER.as_feature_indices(
        [
            'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD',
            'TAX', 'PTRATIO', 'B', 'LSTAT'
        ]
    )

    # These features contain a relatively small number of unique items.

    categorical = HEADER.as_feature_indices(
        ['ZN', 'INDUS', 'CHAS', 'NOX', 'RAD', 'TAX', 'PTRATIO']
    )

    numeric_processors = Pipeline(
        steps=[
            (
                'featureunion',
                FeatureUnion(
                    [
                        ('robust_imputer', RobustImputer()),
                        ('robust_missing_indicator', RobustMissingIndicator())
                    ]
                )
            ),
            (
                'quantileextremevaluestransformer',
                QuantileExtremeValuesTransformer()
            )
        ]
    )

    categorical_processors = Pipeline(
        steps=[('thresholdonehotencoder', ThresholdOneHotEncoder(threshold=9))]
    )

    column_transformer = ColumnTransformer(
        transformers=[
            ('numeric_processing', numeric_processors, numeric
            ), ('categorical_processing', categorical_processors, categorical)
        ]
    )

    return Pipeline(
        steps=[
            ('column_transformer',
             column_transformer), ('robustpca', RobustPCA(n_components=26)),
            ('robuststandardscaler', RobustStandardScaler())
        ]
    )


def build_label_transform():
    """Returns the model definition representing feature processing."""

    return NALabelEncoder()
