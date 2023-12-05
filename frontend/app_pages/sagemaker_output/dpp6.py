from sagemaker_sklearn_extension.externals import Header
from sagemaker_sklearn_extension.impute import RobustImputer
from sagemaker_sklearn_extension.preprocessing import NALabelEncoder
from sagemaker_sklearn_extension.preprocessing import RobustStandardScaler
from sklearn.compose import ColumnTransformer
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

    numeric_processors = Pipeline(
        steps=[
            ('robustimputer',
             RobustImputer()), ('robuststandardscaler', RobustStandardScaler())
        ]
    )

    column_transformer = ColumnTransformer(
        transformers=[('numeric_processing', numeric_processors, numeric)]
    )

    return Pipeline(steps=[('column_transformer', column_transformer)])


def build_label_transform():
    """Returns the model definition representing feature processing."""

    return NALabelEncoder()
