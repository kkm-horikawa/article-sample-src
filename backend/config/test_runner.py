"""pytest を使用するカスタムテストランナー。

このモジュールは、Django の標準テストランナーを pytest に置き換えるための
カスタムテストランナーを定義します。
"""

from django.test.runner import DiscoverRunner


class PytestTestRunner(DiscoverRunner):
    """pytest を使用してテストを実行するカスタムテストランナー。

    Django の manage.py test コマンドで pytest を使用できるようにします。
    """

    def run_tests(self, test_labels, **kwargs):
        """pytest を使用してテストを実行する。

        Args:
            test_labels (list[str]): 実行するテストのラベル
            **kwargs: 追加のキーワード引数

        Returns:
            int: pytest の終了コード（0: 成功、1以上: 失敗）
        """
        import pytest

        argv = ["pytest"]
        if test_labels:
            argv.extend(test_labels)
        else:
            argv.append("api/tests")

        return pytest.main(argv)
