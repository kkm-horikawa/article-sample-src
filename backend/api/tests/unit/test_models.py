"""TODOモデルのユニットテスト。

このモジュールは、TODOモデルの各種機能をテストします。
良いテスト例、悪いテスト例、優先度の低いテスト例に分類しています。
"""

from datetime import date, timedelta

import pytest

from api.models.todo import Todo


@pytest.mark.django_db
class TestTodoModelGoodExamples:
    """TODOモデルの良いテスト例。

    このテストクラスは、効果的で保守性の高いテストの書き方を示しています。
    境界値テスト、同値分割、ハッピーパスなど、実用的なテストパターンを含みます。
    """

    def test_create_todo_with_valid_data(self):
        """有効なデータでTODOを作成できることを確認する。

        【テストの意図】
        すべてのフィールドに有効な値を設定してTODOを作成し、
        データが正しく保存されることを保証します。

        【何を保証するか】
        - すべてのフィールドに値を設定してTODOを作成できること
        - 作成されたTODOの各フィールドの値が期待通りであること
        - IDが自動採番されること
        - completedフィールドがデフォルト値(False)になること

        【テスト手順】
        1. 全フィールドに値を設定してTODOを作成
        2. 作成されたTODOの各フィールド値を検証

        【期待する結果】
        各フィールドの値が設定した値と一致すること
        """
        todo = Todo.objects.create(
            title="Buy groceries",
            description="Milk, eggs, bread",
            priority=Todo.PRIORITY_HIGH,
            due_date=date.today() + timedelta(days=1),
        )

        assert todo.id is not None
        assert todo.title == "Buy groceries"
        assert todo.description == "Milk, eggs, bread"
        assert todo.priority == Todo.PRIORITY_HIGH
        assert todo.completed is False
        assert todo.due_date == date.today() + timedelta(days=1)

    def test_title_boundary_empty_string(self):
        """境界値テスト: 空文字列のタイトルでTODOを作成できることを確認する。

        【テストの意図】
        タイトルの最小境界値（0文字）でTODOを作成できることを確認します。
        Djangoモデルレベルでは空文字列を許可するため、データベースに保存できます。
        （注: Serializerレベルでは空文字列を拒否する）

        【何を保証するか】
        - 空文字列のタイトルでモデルインスタンスを作成できること
        - 空文字列がそのまま保存されること

        【テスト手順】
        1. 空文字列のタイトルでTODOを作成
        2. 保存されたタイトルが空文字列であることを確認

        【期待する結果】
        タイトルが空文字列として保存される
        """
        todo = Todo.objects.create(title="")
        assert todo.title == ""

    def test_title_boundary_max_length(self):
        """境界値テスト: 最大文字数(200文字)のタイトルでTODOを作成できることを確認する。

        【テストの意図】
        タイトルの最大境界値（200文字）でTODOが正常に作成できることを確認します。
        CharFieldのmax_length=200の境界値テストです。

        【何を保証するか】
        - 200文字のタイトルでTODOを作成できること
        - タイトルが200文字として正しく保存されること

        【テスト手順】
        1. 200文字の文字列をタイトルに設定してTODOを作成
        2. 保存されたタイトルの文字数が200であることを確認

        【期待する結果】
        200文字のタイトルが正常に保存される
        """
        max_title = "a" * 200
        todo = Todo.objects.create(title=max_title)
        assert len(todo.title) == 200

    def test_title_boundary_exceeds_max_length(self):
        """境界値テスト: 最大文字数を超えるタイトルの動作を確認する。

        【テストの意図】
        タイトルの境界値を超えた場合の動作を確認します。
        SQLiteはmax_lengthを厳密にチェックしないため、201文字でも保存されます。
        （注: PostgreSQLなど他のDBでは例外が発生する可能性があります）

        【何を保証するか】
        - SQLiteでは201文字のタイトルも保存できること（DB依存の動作）
        - データベースの制約がゆるい場合の動作を確認

        【テスト手順】
        1. 201文字の文字列をタイトルに設定してTODOを作成
        2. SQLiteでは保存されることを確認

        【期待する結果】
        SQLiteでは201文字のタイトルが保存される（DB依存）
        """
        todo = Todo.objects.create(title="a" * 201)
        assert len(todo.title) == 201

    def test_priority_equivalence_valid_values(self):
        """同値分割テスト: 有効な優先度の値でTODOを作成できることを確認する。

        【テストの意図】
        優先度フィールドの有効な値（low/medium/high）すべてでTODOを作成でき、
        各値が正しく保存されることを確認します。同値分割の正常系テストです。

        【何を保証するか】
        - 3つの有効な優先度の値すべてでTODOを作成できること
        - 各優先度の値が正しく保存されること

        【テスト手順】
        1. 各優先度（low/medium/high）でTODOを作成
        2. 保存された優先度の値が設定した値と一致することを確認

        【期待する結果】
        すべての有効な優先度の値でTODOが作成され、値が正しく保存される
        """
        for priority in [Todo.PRIORITY_LOW, Todo.PRIORITY_MEDIUM, Todo.PRIORITY_HIGH]:
            todo = Todo.objects.create(title=f"TODO {priority}", priority=priority)
            assert todo.priority == priority

    def test_priority_equivalence_invalid_value(self):
        """同値分割テスト: 無効な優先度の値の動作を確認する。

        【テストの意図】
        優先度フィールドに無効な値を設定した場合の動作を確認します。
        Djangoモデルレベルではchoicesのバリデーションが実行されないため、
        無効な値も保存されます。（注: Serializerレベルでバリデーションされる）

        【何を保証するか】
        - モデルレベルでは無効な優先度の値も保存できること
        - データベースに無効な値が保存された場合の動作を確認

        【テスト手順】
        1. 無効な優先度（super_high）でTODOを作成
        2. 無効な値がそのまま保存されることを確認

        【期待する結果】
        モデルレベルでは無効な優先度も保存される（Serializer で防ぐ）
        """
        todo = Todo.objects.create(title="Invalid Priority", priority="super_high")
        assert todo.priority == "super_high"

    def test_is_overdue_with_past_date(self):
        """is_overdueメソッドのテスト: 過去の期限日の場合。

        【テストの意図】
        期限日が過去の日付で、未完了のTODOが期限切れと判定されることを確認します。

        【何を保証するか】
        - 期限日が昨日のTODOがis_overdue()でTrueを返すこと
        - 期限切れの判定ロジックが正しく動作すること

        【テスト手順】
        1. 期限日を昨日に設定してTODOを作成
        2. is_overdue()がTrueを返すことを確認

        【期待する結果】
        is_overdue()がTrueを返す
        """
        todo = Todo.objects.create(
            title="Overdue task",
            due_date=date.today() - timedelta(days=1),
        )
        assert todo.is_overdue() is True

    def test_is_overdue_with_future_date(self):
        """is_overdueメソッドのテスト: 未来の期限日の場合。

        【テストの意図】
        期限日が未来の日付のTODOは期限切れでないことを確認します。

        【何を保証するか】
        - 期限日が明日のTODOがis_overdue()でFalseを返すこと
        - 期限前のTODOが期限切れと判定されないこと

        【テスト手順】
        1. 期限日を明日に設定してTODOを作成
        2. is_overdue()がFalseを返すことを確認

        【期待する結果】
        is_overdue()がFalseを返す
        """
        todo = Todo.objects.create(
            title="Future task",
            due_date=date.today() + timedelta(days=1),
        )
        assert todo.is_overdue() is False

    def test_is_overdue_with_today_date(self):
        """is_overdueメソッドのテスト: 今日が期限日の場合。

        【テストの意図】
        期限日が今日のTODOは期限切れではないことを確認します。
        期限日当日はまだ期限切れではありません。

        【何を保証するか】
        - 期限日が今日のTODOがis_overdue()でFalseを返すこと
        - 期限日当日は期限切れと判定されないこと

        【テスト手順】
        1. 期限日を今日に設定してTODOを作成
        2. is_overdue()がFalseを返すことを確認

        【期待する結果】
        is_overdue()がFalseを返す
        """
        todo = Todo.objects.create(
            title="Today's task",
            due_date=date.today(),
        )
        assert todo.is_overdue() is False

    def test_is_overdue_with_null_date(self):
        """is_overdueメソッドのテスト: 期限日が未設定の場合。

        【テストの意図】
        期限日が設定されていないTODOは期限切れにならないことを確認します。

        【何を保証するか】
        - 期限日がNullのTODOがis_overdue()でFalseを返すこと
        - 期限日なしのTODOが期限切れと判定されないこと

        【テスト手順】
        1. 期限日をNullに設定してTODOを作成
        2. is_overdue()がFalseを返すことを確認

        【期待する結果】
        is_overdue()がFalseを返す
        """
        todo = Todo.objects.create(
            title="No deadline task",
            due_date=None,
        )
        assert todo.is_overdue() is False

    def test_is_overdue_completed_task(self):
        """is_overdueメソッドのテスト: 完了済みタスクの場合。

        【テストの意図】
        期限日が過去でも、完了済みのTODOは期限切れと判定されないことを確認します。
        完了したタスクは期限切れの対象外です。

        【何を保証するか】
        - 完了済みで期限日が過去のTODOがis_overdue()でFalseを返すこと
        - 完了済みタスクが期限切れリストに表示されないこと

        【テスト手順】
        1. 期限日を昨日、完了状態をTrueに設定してTODOを作成
        2. is_overdue()がFalseを返すことを確認

        【期待する結果】
        is_overdue()がFalseを返す
        """
        todo = Todo.objects.create(
            title="Completed overdue task",
            due_date=date.today() - timedelta(days=1),
            completed=True,
        )
        assert todo.is_overdue() is False

    def test_get_priority_display_ja(self):
        """get_priority_display_jaメソッドのテスト。

        【テストの意図】
        優先度の英語表記（low/medium/high）が正しく日本語表記（低/中/高）に
        変換されることを確認します。

        【何を保証するか】
        - 各優先度の値が正しい日本語表記に変換されること
        - すべての優先度パターンで変換が動作すること

        【テスト手順】
        1. 各優先度（low/medium/high）でTODOを作成
        2. get_priority_display_ja()が対応する日本語を返すことを確認

        【期待する結果】
        low→低、medium→中、high→高 と変換される
        """
        test_cases = [
            (Todo.PRIORITY_LOW, "低"),
            (Todo.PRIORITY_MEDIUM, "中"),
            (Todo.PRIORITY_HIGH, "高"),
        ]

        for priority, expected_ja in test_cases:
            todo = Todo.objects.create(title="Test", priority=priority)
            assert todo.get_priority_display_ja() == expected_ja

    def test_default_values(self):
        """デフォルト値のテスト。

        【テストの意図】
        必須フィールド以外を省略してTODOを作成した場合、
        各フィールドが適切なデフォルト値になることを確認します。

        【何を保証するか】
        - completedフィールドのデフォルト値がFalseであること
        - priorityフィールドのデフォルト値がmediumであること
        - descriptionフィールドのデフォルト値が空文字列であること
        - due_dateフィールドのデフォルト値がNoneであること

        【テスト手順】
        1. タイトルのみを指定してTODOを作成
        2. 各フィールドのデフォルト値を確認

        【期待する結果】
        各フィールドが定義されたデフォルト値になる
        """
        todo = Todo.objects.create(title="Minimal TODO")

        assert todo.completed is False
        assert todo.priority == Todo.PRIORITY_MEDIUM
        assert todo.description == ""
        assert todo.due_date is None


@pytest.mark.django_db
class TestTodoModelBadExamples:
    """TODOモデルの悪いテスト例。

    このテストクラスは、避けるべきテストパターンを示しています。
    これらのテストは意味がない、メンテナンスコストが高い、または
    実装の詳細に依存しすぎているため、良いテストとは言えません。
    """

    def test_always_passes(self):
        """❌ 悪いテスト: 常にパスするテスト。

        【なぜ悪いか】
        このテストは何も検証していません。常にTrueをアサートするだけで、
        コードの動作を何も保証していません。テストカバレッジを上げるだけの
        無意味なテストです。

        【問題点】
        - コードの動作を何も検証していない
        - バグを検出できない
        - テストの存在意義がない
        """
        assert True

    def test_implementation_detail(self):
        """❌ 悪いテスト: 実装の内部詳細をテストしている。

        【なぜ悪いか】
        Djangoの内部実装（_state、_meta）をテストしています。
        これらは公開APIではなく、Djangoのバージョンアップで変更される可能性があります。
        実装の詳細に依存したテストは、リファクタリングの妨げになります。

        【問題点】
        - Djangoの内部実装に依存している
        - フレームワークのアップデートで壊れる可能性が高い
        - ビジネスロジックを検証していない
        """
        todo = Todo.objects.create(title="Test")

        assert todo._state.db == "default"
        assert hasattr(todo, "_meta")

    def test_django_framework_behavior(self):
        """❌ 悪いテスト: フレームワークの動作をテストしている。

        【なぜ悪いか】
        IDの自動採番はDjangoフレームワークが保証する機能です。
        フレームワークの動作をテストしても、アプリケーション固有の
        ビジネスロジックは何も検証できません。

        【問題点】
        - Djangoフレームワークの動作をテストしている
        - アプリケーション固有のロジックを検証していない
        - Djangoが既にテストしている内容の重複
        """
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")

        assert todo2.id > todo1.id


@pytest.mark.django_db
class TestTodoModelLowPriorityExamples:
    """TODOモデルの優先度の低いテスト例。

    このテストクラスは、必ずしも不要ではないが、優先度が低いテストを示しています。
    単純なgetter/setterや設定値の確認など、バグが発生しにくい箇所のテストです。
    """

    def test_str_method(self):
        """🔻 低優先度: __str__メソッドのテスト。

        【なぜ優先度が低いか】
        __str__メソッドは単純にtitleを返すだけで、複雑なロジックはありません。
        このようなシンプルなメソッドはバグが発生しにくく、テストの優先度は低いです。

        【いつテストするか】
        - __str__に複雑なフォーマット処理がある場合
        - 管理画面で表示が重要な場合
        - 時間に余裕がある場合
        """
        todo = Todo.objects.create(title="Test TODO")
        assert str(todo) == "Test TODO"

    def test_meta_ordering(self):
        """🔻 低優先度: Meta.orderingの設定値確認。

        【なぜ優先度が低いか】
        Meta.orderingは設定値の確認であり、ロジックのテストではありません。
        設定ミスはすぐに気づくため、テストの必要性は低いです。

        【いつテストするか】
        - ソート順が複雑で重要なビジネスロジックの場合
        - デフォルトの並び順が要件として明確に定義されている場合
        """
        assert Todo._meta.ordering == ["-created_at"]

    def test_meta_db_table(self):
        """🔻 低優先度: Meta.db_tableの設定値確認。

        【なぜ優先度が低いか】
        テーブル名の確認は設定値のテストであり、ビジネスロジックではありません。
        マイグレーション実行時にテーブルが作成されないなど、他の方法で検出できます。

        【いつテストするか】
        - 既存のレガシーテーブルとの互換性が重要な場合
        - テーブル名の命名規則が厳密に定義されている場合
        """
        assert Todo._meta.db_table == "todos"
