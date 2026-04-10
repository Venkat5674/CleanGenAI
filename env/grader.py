import pandas as pd


def grade(output_df: pd.DataFrame, expected_df: pd.DataFrame) -> float:
    try:
        if (
            output_df is None
            or expected_df is None
            or output_df.empty
            or expected_df.empty
        ):
            return 0.01

        output_df = output_df.sort_values(by=list(output_df.columns)).reset_index(
            drop=True
        )
        expected_df = expected_df.sort_values(by=list(expected_df.columns)).reset_index(
            drop=True
        )

        if len(output_df) != len(expected_df) or len(output_df.columns) != len(
            expected_df.columns
        ):
            return 0.01

        matches = ((output_df == expected_df) | (output_df.isna() & expected_df.isna())).sum().sum()
        total = output_df.size

        score = matches / total
        return float(max(0.01, min(0.99, score)))
    except Exception:
        return 0.01
