"""TODO API統合テスト。

このモジュールは、TODO APIのエンドポイントをHTTPリクエストレベルでテストします。
REST APIの各操作(CRUD、カスタムアクション)が正しく動作することを検証します。
良いテスト例、悪いテスト例に分類しています。
"""

from datetime import date, timedelta

import pytest

from api.models.todo import Todo


@pytest.mark.django_db
class TestTodoAPIListGoodExamples:
    """TODO一覧取得APIの良いテスト例。

    このテストクラスは、GET /api/todos/ エンドポイントの
    効果的なテスト方法を示しています。
    """

    def test_get_all_todos(self, api_client, multiple_todos):
        """全TODO取得APIが正しく動作することを確認する。

        【テストの意図】
        GET /api/todos/ が全TODOを取得し、正しいレスポンス形式で
        返すことを保証します。

        【何を保証するか】
        - ステータスコードが200であること
        - レスポンスにcount(全件数)が含まれること
        - レスポンスのresultsに全TODOが含まれること

        【テスト手順】
        1. multiple_todosフィクスチャで10件のTODOを作成
        2. GET /api/todos/ を呼び出し
        3. ステータスコードとレスポンス内容を検証

        【期待する結果】
        - ステータスコード: 200
        - count: 10
        - results配列の長さ: 10
        """
        response = api_client.get("/api/todos/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 10
        assert len(data["results"]) == 10

    def test_filter_by_completed(self, api_client, multiple_todos):
        """完了状態でフィルタリングするAPIが正しく動作することを確認する。

        【テストの意図】
        GET /api/todos/?completed=true が完了済みTODOのみを返すことを保証します。

        【何を保証するか】
        - ステータスコードが200であること
        - 返されるすべてのTODOのcompletedがtrueであること

        【テスト手順】
        1. multiple_todosフィクスチャでTODOを作成
        2. GET /api/todos/?completed=true を呼び出し
        3. レスポンス内容を検証

        【期待する結果】
        - ステータスコード: 200
        - すべてのTODOのcompletedがtrueであること
        """
        response = api_client.get("/api/todos/?completed=true")

        assert response.status_code == 200
        data = response.json()
        assert all(todo["completed"] for todo in data["results"])

    def test_filter_by_priority(self, api_client, multiple_todos):
        """優先度でフィルタリングするAPIが正しく動作することを確認する。

        【テストの意図】
        GET /api/todos/?priority=high が指定した優先度のTODOのみを返すことを保証します。

        【何を保証するか】
        - ステータスコードが200であること
        - 返されるすべてのTODOのpriorityが"high"であること

        【テスト手順】
        1. multiple_todosフィクスチャで様々な優先度のTODOを作成
        2. GET /api/todos/?priority=high を呼び出し
        3. レスポンス内容を検証

        【期待する結果】
        - ステータスコード: 200
        - すべてのTODOのpriorityが"high"であること
        """
        response = api_client.get("/api/todos/?priority=high")

        assert response.status_code == 200
        data = response.json()
        assert all(todo["priority"] == "high" for todo in data["results"])

    def test_empty_list(self, api_client):
        """TODOが存在しない場合のAPIレスポンスを確認する。

        【テストの意図】
        GET /api/todos/ がTODOが0件の場合に空配列を返すことを保証します。

        【何を保証するか】
        - ステータスコードが200であること
        - countが0であること
        - resultsが空配列であること

        【テスト手順】
        1. TODOを作成せずにGET /api/todos/ を呼び出し
        2. ステータスコードとレスポンス内容を検証

        【期待する結果】
        - ステータスコード: 200
        - count: 0
        - results: []
        """
        response = api_client.get("/api/todos/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["results"] == []


@pytest.mark.django_db
class TestTodoAPICreateGoodExamples:
    """TODO作成APIの良いテスト例。

    このテストクラスは、POST /api/todos/ エンドポイントの
    効果的なテスト方法を示しています。
    """

    def test_create_todo_with_all_fields(self, api_client):
        """全フィールド指定でTODO作成APIが正しく動作することを確認する。

        【テストの意図】
        POST /api/todos/ が全フィールドを指定してTODOを作成し、
        201ステータスと作成されたTODOを返すことを保証します。

        【何を保証するか】
        ステータスコードが201であること、
        レスポンスに作成されたTODOの情報が含まれること

        【テスト手順】
        全フィールドを含むJSONデータを準備 →
        POST /api/todos/を呼び出し →
        ステータスコードとレスポンス内容を検証

        【期待する結果】
        ステータスコード201、レスポンスに指定した値が反映されていること
        """
        data = {
            "title": "New TODO",
            "description": "Description",
            "priority": "high",
            "due_date": str(date.today() + timedelta(days=1)),
        }
        response = api_client.post(
            "/api/todos/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 201
        response_data = response.json()
        assert response_data["title"] == "New TODO"
        assert response_data["description"] == "Description"
        assert response_data["priority"] == "high"

    def test_create_todo_minimal_fields(self, api_client):
        """最小限のフィールドでTODO作成APIが正しく動作することを確認する。

        【テストの意図】POST /api/todos/ がタイトルのみでTODOを作成し、デフォルト値が正しく設定されることを保証します。
        【何を保証するか】ステータスコードが201、completedがfalse、priorityが"medium"にデフォルト設定されること
        【テスト手順】タイトルのみのJSONデータを準備→POST /api/todos/を呼び出し→ステータスコードとデフォルト値を検証
        【期待する結果】ステータスコード201、デフォルト値が正しく設定されること
        """
        data = {"title": "Minimal TODO"}
        response = api_client.post(
            "/api/todos/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 201
        response_data = response.json()
        assert response_data["title"] == "Minimal TODO"
        assert response_data["completed"] is False
        assert response_data["priority"] == "medium"

    def test_create_todo_boundary_title_max_length(self, api_client):
        """最大文字数(200文字)のタイトルでTODO作成APIが正しく動作することを確認する。

        【テストの意図】境界値テストとして、最大文字数(200文字)のタイトルでTODOが正しく作成されることを保証します。
        【何を保証するか】ステータスコードが201であること、200文字のタイトルでTODOが作成されること
        【テスト手順】200文字のタイトルを持つJSONデータを準備→POST /api/todos/を呼び出し→ステータスコードを検証
        【期待する結果】ステータスコード201
        """
        data = {"title": "a" * 200}
        response = api_client.post(
            "/api/todos/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 201

    def test_create_todo_invalid_empty_title(self, api_client):
        """空文字列のタイトルでTODO作成が拒否されることを確認する。

        【テストの意図】バリデーションエラーのテストとして、空文字列のタイトルでAPI呼び出しが400エラーを返すことを保証します。
        【何を保証するか】ステータスコードが400であること、エラーレスポンスにtitleフィールドが含まれること
        【テスト手順】空文字列のタイトルを持つJSONデータを準備→POST /api/todos/を呼び出し→ステータスコードとエラー内容を検証
        【期待する結果】ステータスコード400、エラーレスポンスに"title"が含まれること
        """
        data = {"title": ""}
        response = api_client.post(
            "/api/todos/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "title" in response.json()

    def test_create_todo_invalid_title_exceeds_max_length(self, api_client):
        """最大文字数を超えるタイトルでTODO作成が拒否されることを確認する。

        【テストの意図】境界値テストとして、201文字のタイトルでAPI呼び出しが400エラーを返すことを保証します。
        【何を保証するか】ステータスコードが400であること
        【テスト手順】201文字のタイトルを持つJSONデータを準備→POST /api/todos/を呼び出し→ステータスコードを検証
        【期待する結果】ステータスコード400
        """
        data = {"title": "a" * 201}
        response = api_client.post(
            "/api/todos/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 400

    def test_create_todo_invalid_priority(self, api_client):
        """無効な優先度でTODO作成が拒否されることを確認する。

        【テストの意図】バリデーションエラーのテストとして、無効な優先度値でAPI呼び出しが400エラーを返すことを保証します。
        【何を保証するか】ステータスコードが400であること、エラーレスポンスにpriorityフィールドが含まれること
        【テスト手順】無効な優先度を持つJSONデータを準備→POST /api/todos/を呼び出し→ステータスコードとエラー内容を検証
        【期待する結果】ステータスコード400、エラーレスポンスに"priority"が含まれること
        """
        data = {"title": "Test", "priority": "super_high"}
        response = api_client.post(
            "/api/todos/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "priority" in response.json()


@pytest.mark.django_db
class TestTodoAPIRetrieveGoodExamples:
    """TODO詳細取得APIの良いテスト例。このテストクラスは、GET /api/todos/{id}/ エンドポイントの効果的なテスト方法を示しています。"""

    def test_get_existing_todo(self, api_client, sample_todo):
        """存在するTODOの詳細を取得できることを確認する。

        【テストの意図】GET /api/todos/{id}/ が指定したIDのTODOを正しく取得できることを保証します。
        【何を保証するか】ステータスコードが200であること、指定したIDのTODOの詳細が返されること
        【テスト手順】sample_todoを作成→GET /api/todos/{id}/を呼び出し→ステータスコードとレスポンス内容を検証
        【期待する結果】ステータスコード200、レスポンスにTODOの詳細が含まれること
        """
        response = api_client.get(f"/api/todos/{sample_todo.id}/")

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == sample_todo.id
        assert response_data["title"] == sample_todo.title

    def test_get_nonexistent_todo(self, api_client):
        """存在しないTODOのIDで404エラーが返されることを確認する。

        【テストの意図】GET /api/todos/{id}/ が存在しないIDに対して404エラーを返すことを保証します。
        【何を保証するか】ステータスコードが404であること
        【テスト手順】存在しないID(99999)でGET /api/todos/{id}/を呼び出し→ステータスコードを検証
        【期待する結果】ステータスコード404
        """
        response = api_client.get("/api/todos/99999/")

        assert response.status_code == 404


@pytest.mark.django_db
class TestTodoAPIUpdateGoodExamples:
    """TODO更新APIの良いテスト例。このテストクラスは、PATCH /api/todos/{id}/ エンドポイントの効果的なテスト方法を示しています。"""

    def test_update_todo_title(self, api_client, sample_todo):
        """TODOのタイトルを更新できることを確認する。

        【テストの意図】PATCH /api/todos/{id}/ がTODOのタイトルを正しく更新できることを保証します。
        【何を保証するか】ステータスコードが200であること、タイトルが更新されること、データベースに反映されること
        【テスト手順】sample_todoを作成→PATCH /api/todos/{id}/で更新→レスポンスとDBを検証
        【期待する結果】ステータスコード200、タイトルが更新されること
        """
        data = {"title": "Updated Title"}
        response = api_client.patch(
            f"/api/todos/{sample_todo.id}/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

        sample_todo.refresh_from_db()
        assert sample_todo.title == "Updated Title"

    def test_update_todo_completed(self, api_client, sample_todo):
        """TODOの完了状態を更新できることを確認する。

        【テストの意図】PATCH /api/todos/{id}/ がTODOの完了状態を正しく更新できることを保証します。
        【何を保証するか】ステータスコードが200であること、completedがtrueに更新されること
        【テスト手順】sample_todoを作成→PATCH /api/todos/{id}/でcompleted=trueを更新→レスポンスを検証
        【期待する結果】ステータスコード200、completedがtrueになること
        """
        data = {"completed": True}
        response = api_client.patch(
            f"/api/todos/{sample_todo.id}/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_update_todo_invalid_data(self, api_client, sample_todo):
        """無効なデータでTODO更新が拒否されることを確認する。

        【テストの意図】PATCH /api/todos/{id}/ が無効なデータに対して400エラーを返すことを保証します。
        【何を保証するか】ステータスコードが400であること
        【テスト手順】sample_todoを作成→PATCH /api/todos/{id}/で空文字列のタイトルを送信→ステータスコードを検証
        【期待する結果】ステータスコード400
        """
        data = {"title": ""}
        response = api_client.patch(
            f"/api/todos/{sample_todo.id}/",
            data=data,
            content_type="application/json",
        )

        assert response.status_code == 400


@pytest.mark.django_db
class TestTodoAPIDeleteGoodExamples:
    """TODO削除APIの良いテスト例。このテストクラスは、DELETE /api/todos/{id}/ エンドポイントの効果的なテスト方法を示しています。"""

    def test_delete_existing_todo(self, api_client, sample_todo):
        """存在するTODOを削除できることを確認する。

        【テストの意図】DELETE /api/todos/{id}/ がTODOを正しく削除できることを保証します。
        【何を保証するか】ステータスコードが204であること、データベースからTODOが削除されること
        【テスト手順】sample_todoを作成→DELETE /api/todos/{id}/を呼び出し→ステータスコードとDB状態を検証
        【期待する結果】ステータスコード204、データベースにTODOが存在しないこと
        """
        todo_id = sample_todo.id
        response = api_client.delete(f"/api/todos/{todo_id}/")

        assert response.status_code == 204
        assert not Todo.objects.filter(id=todo_id).exists()

    def test_delete_nonexistent_todo(self, api_client):
        """存在しないTODOの削除で404エラーが返されることを確認する。

        【テストの意図】DELETE /api/todos/{id}/ が存在しないIDに対して404エラーを返すことを保証します。
        【何を保証するか】ステータスコードが404であること
        【テスト手順】存在しないID(99999)でDELETE /api/todos/{id}/を呼び出し→ステータスコードを検証
        【期待する結果】ステータスコード404
        """
        response = api_client.delete("/api/todos/99999/")

        assert response.status_code == 404


@pytest.mark.django_db
class TestTodoAPIToggleGoodExamples:
    """TODO完了状態切り替えAPIの良いテスト例。このテストクラスは、POST /api/todos/{id}/toggle/ エンドポイントの効果的なテスト方法を示しています。"""

    def test_toggle_incomplete_to_complete(self, api_client, sample_todo):
        """未完了TODOを完了に切り替えられることを確認する。

        【テストの意図】POST /api/todos/{id}/toggle/ が未完了TODOを完了に切り替えられることを保証します。
        【何を保証するか】ステータスコードが200であること、completedがtrueに変更されること
        【テスト手順】未完了sample_todoを作成→POST /api/todos/{id}/toggle/を呼び出し→レスポンスを検証
        【期待する結果】ステータスコード200、completedがtrueになること
        """
        assert sample_todo.completed is False

        response = api_client.post(f"/api/todos/{sample_todo.id}/toggle/")

        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_toggle_complete_to_incomplete(self, api_client, completed_todo):
        """完了TODOを未完了に切り替えられることを確認する。

        【テストの意図】POST /api/todos/{id}/toggle/ が完了TODOを未完了に切り替えられることを保証します。
        【何を保証するか】ステータスコードが200であること、completedがfalseに変更されること
        【テスト手順】完了completed_todoを作成→POST /api/todos/{id}/toggle/を呼び出し→レスポンスを検証
        【期待する結果】ステータスコード200、completedがfalseになること
        """
        assert completed_todo.completed is True

        response = api_client.post(f"/api/todos/{completed_todo.id}/toggle/")

        assert response.status_code == 200
        assert response.json()["completed"] is False


@pytest.mark.django_db
class TestTodoAPIBulkDeleteGoodExamples:
    """TODO一括削除APIの良いテスト例。このテストクラスは、DELETE /api/todos/bulk_delete_completed/ エンドポイントの効果的なテスト方法を示しています。"""

    def test_bulk_delete_completed(self, api_client):
        """完了済みTODOを一括削除できることを確認する。

        【テストの意図】DELETE /api/todos/bulk_delete_completed/ が完了済みTODOのみを削除し、削除件数を返すことを保証します。
        【何を保証するか】ステータスコードが200であること、完了TODO2件が削除されること、未完了TODOは残ること
        【テスト手順】完了TODO2件と未完了TODO1件を作成→DELETE /api/todos/bulk_delete_completed/を呼び出し→レスポンスとDB状態を検証
        【期待する結果】ステータスコード200、deleted_countが2、未完了TODO1件のみ残ること
        """
        Todo.objects.create(title="Completed 1", completed=True)
        Todo.objects.create(title="Completed 2", completed=True)
        Todo.objects.create(title="Active", completed=False)

        response = api_client.delete("/api/todos/bulk_delete_completed/")

        assert response.status_code == 200
        assert response.json()["deleted_count"] == 2
        assert Todo.objects.count() == 1


@pytest.mark.django_db
class TestTodoAPIStatisticsGoodExamples:
    """TODO統計情報APIの良いテスト例。このテストクラスは、GET /api/todos/statistics/ エンドポイントの効果的なテスト方法を示しています。"""

    def test_get_statistics(self, api_client):
        """TODO統計情報を取得できることを確認する。

        【テストの意図】GET /api/todos/statistics/ が全件数、完了件数、未完了件数、期限切れ件数を正しく集計することを保証します。
        【何を保証するか】ステータスコードが200であること、各統計値が正しく集計されること
        【テスト手順】完了TODO1件、未完了TODO1件、期限切れTODO1件を作成→GET /api/todos/statistics/を呼び出し→レスポンスを検証
        【期待する結果】ステータスコード200、total:3、completed:1、pending:2、overdue:1
        """
        Todo.objects.create(title="Completed", completed=True)
        Todo.objects.create(title="Active", completed=False)
        Todo.objects.create(
            title="Overdue",
            completed=False,
            due_date=date.today() - timedelta(days=1),
        )

        response = api_client.get("/api/todos/statistics/")

        assert response.status_code == 200
        stats = response.json()
        assert stats["total"] == 3
        assert stats["completed"] == 1
        assert stats["pending"] == 2
        assert stats["overdue"] == 1


@pytest.mark.django_db
class TestTodoAPIBadExamples:
    """TODO APIの悪いテスト例。このテストクラスは、避けるべきテストパターンを示しています。"""

    def test_api_always_returns_200(self, api_client):
        """【悪い例】APIが常に成功ステータスを返すかをチェックする。

        このテストが悪い理由:
        - 複数のステータスコードを許容しており、具体的な動作を検証していない
        - 常にtrueになる条件で実質的に何も検証していない
        - APIの具体的な仕様を保証していない

        改善方法:
        特定のエンドポイントに対して、期待される具体的なステータスコードを検証すべき
        """
        response = api_client.get("/api/todos/")
        assert response.status_code in [200, 201, 204, 400, 404]

    def test_response_has_content_type(self, api_client):
        """【悪い例】レスポンスにContent-Typeヘッダーが含まれるかをチェックする。

        このテストが悪い理由:
        - HTTPフレームワークが保証する内容をテストしている
        - Content-Typeの具体的な値を検証していない
        - APIの機能やビジネスロジックを何も保証しない

        改善方法:
        Content-Typeの具体的な値(application/json)を検証するか、
        レスポンスボディの内容を検証すべき
        """
        response = api_client.get("/api/todos/")
        assert "content-type" in response.headers
