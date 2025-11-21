"""ゴールデンデータとスナップショットテストのヘルパー。

このモジュールは、Parquet形式のゴールデンデータを使用した
スナップショットテストをサポートするヘルパークラスを提供します。
"""

from pathlib import Path
from typing import Any

import pandas as pd


class GoldenDataLoader:
    """ゴールデンデータの読み書きを行うクラス。

    Parquet形式でゴールデンデータを保存・読み込みします。
    zstd圧縮により効率的なストレージを実現します。

    Attributes:
        data_dir (Path): ゴールデンデータの格納ディレクトリ
    """

    def __init__(self, data_dir: Path | str):
        """GoldenDataLoaderを初期化する。

        Args:
            data_dir (Path | str): ゴールデンデータの格納ディレクトリパス
        """
        self.data_dir = Path(data_dir)

    def load_parquet(self, filename: str) -> pd.DataFrame:
        """Parquetファイルからゴールデンデータを読み込む。

        Args:
            filename (str): 読み込むファイル名

        Returns:
            pd.DataFrame: 読み込まれたデータフレーム

        Raises:
            FileNotFoundError: ファイルが存在しない場合
        """
        file_path = self.data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Golden data file not found: {file_path}")
        return pd.read_parquet(file_path)

    def save_parquet(self, df: pd.DataFrame, filename: str):
        """データフレームをParquet形式で保存する。

        zstd圧縮（レベル22）を使用して高圧縮率でデータを保存します。

        Args:
            df (pd.DataFrame): 保存するデータフレーム
            filename (str): 保存先ファイル名
        """
        file_path = self.data_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(
            file_path,
            engine="pyarrow",
            compression="zstd",
            compression_level=22,
        )


class SnapshotComparator:
    """スナップショットテストの比較を行うクラス。

    実際のデータとゴールデンデータを比較し、
    一致することを検証します。

    Attributes:
        loader (GoldenDataLoader): ゴールデンデータローダー
    """

    def __init__(self, golden_data_loader: GoldenDataLoader):
        """SnapshotComparatorを初期化する。

        Args:
            golden_data_loader (GoldenDataLoader): ゴールデンデータローダー
        """
        self.loader = golden_data_loader

    def assert_matches_snapshot(
        self,
        actual_data: list[dict[str, Any]],
        snapshot_name: str,
        exclude_fields: list[str] | None = None,
        tolerance: float = 1e-6,
    ):
        """実際のデータとゴールデンデータが一致することを検証する。

        Args:
            actual_data (list[dict[str, Any]]): 検証する実際のデータ
            snapshot_name (str): スナップショット名（ファイル名のベース）
            exclude_fields (list[str] | None): 比較から除外するフィールド
            tolerance (float): 数値比較の許容誤差

        Raises:
            AssertionError: データが一致しない場合
        """
        if exclude_fields is None:
            exclude_fields = []

        actual_df = pd.DataFrame(actual_data)

        for field in exclude_fields:
            if field in actual_df.columns:
                actual_df = actual_df.drop(columns=[field])

        golden_df = self.loader.load_parquet(f"{snapshot_name}.parquet")

        for field in exclude_fields:
            if field in golden_df.columns:
                golden_df = golden_df.drop(columns=[field])

        assert len(actual_df) == len(golden_df), (
            f"Row count mismatch: expected {len(golden_df)}, got {len(actual_df)}"
        )

        assert list(actual_df.columns) == list(golden_df.columns), (
            f"Column mismatch: expected {list(golden_df.columns)}, "
            f"got {list(actual_df.columns)}"
        )

        for col in actual_df.columns:
            actual_series = actual_df[col]
            golden_series = golden_df[col]

            if pd.api.types.is_numeric_dtype(actual_series):
                pd.testing.assert_series_equal(
                    actual_series,
                    golden_series,
                    check_dtype=False,
                    atol=tolerance,
                    rtol=tolerance,
                )
            else:
                pd.testing.assert_series_equal(
                    actual_series,
                    golden_series,
                    check_dtype=False,
                )

    def create_snapshot(
        self,
        data: list[dict[str, Any]],
        snapshot_name: str,
    ):
        """新しいスナップショットを作成する。

        実際のデータからゴールデンデータを生成します。

        Args:
            data (list[dict[str, Any]]): スナップショットとして保存するデータ
            snapshot_name (str): スナップショット名（ファイル名のベース）
        """
        df = pd.DataFrame(data)
        self.loader.save_parquet(df, f"{snapshot_name}.parquet")
