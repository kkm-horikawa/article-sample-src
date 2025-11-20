/**
 * @fileoverview TodoServiceのテスト
 *
 * このファイルは、TodoService（API通信サービス）の各種メソッドをテストします。
 * fetchをモックして、API呼び出しが正しく行われることを検証します。
 * 良いテスト例、悪いテスト例、優先度の低いテスト例に分類しています。
 */

import TodoService from "@/services/TodoService";
import type { Todo, TodoCreate } from "@/types";
import { beforeEach, describe, expect, it, vi } from "vitest";

/** グローバルfetchをモック化 */
global.fetch = vi.fn();

/**
 * モックfetchレスポンスを作成するヘルパー関数
 *
 * @template T - レスポンスデータの型
 * @param {T} data - レスポンスデータ
 * @param {number} [status=200] - HTTPステータスコード
 * @returns {Response} モックレスポンスオブジェクト
 */
function createFetchResponse<T>(data: T, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => data,
    headers: new Headers(),
  } as Response;
}

/** テスト用のモックTODOデータ */
const mockTodo: Todo = {
  id: 1,
  title: "Test TODO",
  description: "Test Description",
  completed: false,
  priority: "medium",
  priority_display_ja: "中",
  due_date: "2025-12-31",
  is_overdue: false,
  created_at: "2025-11-20T10:00:00Z",
  updated_at: "2025-11-20T10:00:00Z",
};

describe("TodoService - Good Examples", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("fetches all todos", async () => {
    /**
     * 全TODO取得APIが正しく呼び出されることを確認する
     *
     * 【テストの意図】getTodosメソッドが正しいエンドポイントにGETリクエストを送信し、レスポンスを返すことを保証します。
     * 【何を保証するか】正しいURL、Content-Typeヘッダーでfetchが呼ばれること、レスポンスが正しく返されること
     * 【テスト手順】fetchをモック→getTodos()を呼び出し→fetch呼び出しとレスポンスを検証
     * 【期待する結果】指定したURLとヘッダーでfetchが呼ばれ、モックデータが返されること
     */
    const mockTodos = [mockTodo];
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(createFetchResponse(mockTodos));

    const todos = await TodoService.getTodos();

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/todos/",
      expect.objectContaining({
        headers: expect.objectContaining({
          "Content-Type": "application/json",
        }),
      }),
    );
    expect(todos).toEqual(mockTodos);
  });

  it("fetches todos with completed filter", async () => {
    /**
     * 完了フィルタ付きTODO取得APIが正しく呼び出されることを確認する
     *
     * 【テストの意図】getTodosメソッドがcompletedパラメータをクエリ文字列として正しく渡すことを保証します。
     * 【何を保証するか】クエリパラメータにcompleted=trueが含まれること
     * 【テスト手順】fetchをモック→getTodos({completed:true})を呼び出し→URLにcompleted=trueが含まれることを検証
     * 【期待する結果】fetchの第1引数にcompleted=trueが含まれること
     */
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(createFetchResponse([]));

    await TodoService.getTodos({ completed: true });

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("completed=true"),
      expect.any(Object),
    );
  });

  it("fetches todos with priority filter", async () => {
    /**
     * 優先度フィルタ付きTODO取得APIが正しく呼び出されることを確認する
     *
     * 【テストの意図】getTodosメソッドがpriorityパラメータをクエリ文字列として正しく渡すことを保証します。
     * 【何を保証するか】クエリパラメータにpriority=highが含まれること
     * 【テスト手順】fetchをモック→getTodos({priority:"high"})を呼び出し→URLにpriority=highが含まれることを検証
     * 【期待する結果】fetchの第1引数にpriority=highが含まれること
     */
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(createFetchResponse([]));

    await TodoService.getTodos({ priority: "high" });

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("priority=high"),
      expect.any(Object),
    );
  });

  it("creates a new todo", async () => {
    /**
     * TODO作成APIが正しく呼び出されることを確認する
     *
     * 【テストの意図】createTodoメソッドが正しいエンドポイントにPOSTリクエストを送信し、JSONボディを送ることを保証します。
     * 【何を保証するか】正しいURL、POSTメソッド、JSONボディでfetchが呼ばれること、レスポンスが返されること
     * 【テスト手順】fetchをモック→createTodo()を呼び出し→fetch呼び出しとレスポンスを検証
     * 【期待する結果】指定したURL、POSTメソッド、JSONボディでfetchが呼ばれ、作成されたTODOが返されること
     */
    const newTodo: TodoCreate = {
      title: "New TODO",
      description: "New Description",
      priority: "high",
    };
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(createFetchResponse(mockTodo, 201));

    const result = await TodoService.createTodo(newTodo);

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/todos/",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify(newTodo),
      }),
    );
    expect(result).toEqual(mockTodo);
  });

  it("updates a todo", async () => {
    /**
     * TODO更新APIが正しく呼び出されることを確認する
     *
     * 【テストの意図】updateTodoメソッドが正しいエンドポイントにPATCHリクエストを送信し、更新データを送ることを保証します。
     * 【何を保証するか】正しいURL、PATCHメソッド、JSONボディでfetchが呼ばれること
     * 【テスト手順】fetchをモック→updateTodo(1, data)を呼び出し→fetch呼び出しを検証
     * 【期待する結果】指定したURL、PATCHメソッド、JSONボディでfetchが呼ばれること
     */
    const updateData = { title: "Updated Title" };
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(createFetchResponse(mockTodo));

    await TodoService.updateTodo(1, updateData);

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/todos/1/",
      expect.objectContaining({
        method: "PATCH",
        body: JSON.stringify(updateData),
      }),
    );
  });

  it("deletes a todo", async () => {
    /**
     * TODO削除APIが正しく呼び出されることを確認する
     *
     * 【テストの意図】deleteTodoメソッドが正しいエンドポイントにDELETEリクエストを送信することを保証します。
     * 【何を保証するか】正しいURL、DELETEメソッドでfetchが呼ばれること
     * 【テスト手順】fetchをモック→deleteTodo(1)を呼び出し→fetch呼び出しを検証
     * 【期待する結果】指定したURL、DELETEメソッドでfetchが呼ばれること
     */
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(createFetchResponse(null, 204));

    await TodoService.deleteTodo(1);

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/todos/1/",
      expect.objectContaining({
        method: "DELETE",
      }),
    );
  });

  it("toggles a todo", async () => {
    /**
     * TODO完了状態切り替えAPIが正しく呼び出されることを確認する
     *
     * 【テストの意図】toggleTodoメソッドが正しいエンドポイントにPOSTリクエストを送信することを保証します。
     * 【何を保証するか】正しいURL（/toggle/）、POSTメソッドでfetchが呼ばれること
     * 【テスト手順】fetchをモック→toggleTodo(1)を呼び出し→fetch呼び出しを検証
     * 【期待する結果】指定したURL、POSTメソッドでfetchが呼ばれること
     */
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(createFetchResponse(mockTodo));

    await TodoService.toggleTodo(1);

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/todos/1/toggle/",
      expect.objectContaining({
        method: "POST",
      }),
    );
  });

  it("throws error on failed request", async () => {
    /**
     * APIエラー時に例外をスローすることを確認する
     *
     * 【テストの意図】API呼び出しが失敗した時、適切なエラーメッセージで例外をスローすることを保証します。
     * 【何を保証するか】404エラー時にdetailメッセージを含む例外がスローされること
     * 【テスト手順】fetchを404エラーでモック→getTodo(999)を呼び出し→例外スローを検証
     * 【期待する結果】"Not found"メッセージで例外がスローされること
     */
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(
      createFetchResponse({ detail: "Not found" }, 404),
    );

    await expect(TodoService.getTodo(999)).rejects.toThrow("Not found");
  });

  it("fetches statistics", async () => {
    /**
     * TODO統計情報取得APIが正しく呼び出されることを確認する
     *
     * 【テストの意図】getStatisticsメソッドが正しいエンドポイントにGETリクエストを送信し、統計情報を返すことを保証します。
     * 【何を保証するか】正しいURL（/statistics/）でfetchが呼ばれること、統計データが返されること
     * 【テスト手順】fetchをモック→getStatistics()を呼び出し→fetch呼び出しとレスポンスを検証
     * 【期待する結果】指定したURLでfetchが呼ばれ、統計データが返されること
     */
    const mockStats = { total: 10, completed: 5, pending: 5, overdue: 2 };
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue(createFetchResponse(mockStats));

    const stats = await TodoService.getStatistics();

    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/todos/statistics/",
      expect.any(Object),
    );
    expect(stats).toEqual(mockStats);
  });
});

describe("TodoService - Bad Examples", () => {
  it("always passes", () => {
    /**
     * 【悪い例】常にtrueを返すテスト
     *
     * このテストが悪い理由:
     * - 実際の機能を何も検証していない
     * - 常に成功するため、バグを検出できない
     * - コードカバレッジを水増しするだけで価値がない
     *
     * 改善方法:
     * 実際のAPI呼び出しやレスポンス処理を検証すべき
     */
    expect(true).toBe(true);
  });

  it("checks if TodoService exists", () => {
    /**
     * 【悪い例】TodoServiceの存在をチェックする
     *
     * このテストが悪い理由:
     * - オブジェクトが定義されているかをチェックしているだけで、機能を検証していない
     * - TypeScriptの型チェックやimport機構が保証する内容をテストしている
     * - 実際のメソッドの動作を何も保証しない
     *
     * 改善方法:
     * 実際のメソッドを呼び出して、入力に対する出力やAPI呼び出しを検証すべき
     */
    expect(TodoService).toBeDefined();
  });
});

describe("TodoService - Low Priority Examples", () => {
  it("has getTodos method", () => {
    /**
     * 【優先度低】getTodosメソッドの存在をチェックする
     *
     * このテストの優先度が低い理由:
     * - メソッドの型をチェックしているだけで、実際の動作を検証していない
     * - TypeScriptの型システムが保証する内容をテストしている
     * - メソッドの引数や戻り値を検証していない
     *
     * 改善方法:
     * メソッドを実際に呼び出して、APIリクエストやレスポンス処理を検証すべき
     */
    expect(typeof TodoService.getTodos).toBe("function");
  });

  it("has createTodo method", () => {
    /**
     * 【優先度低】createTodoメソッドの存在をチェックする
     *
     * このテストの優先度が低い理由:
     * - メソッドの型をチェックしているだけで、実際の動作を検証していない
     * - TypeScriptの型システムが保証する内容をテストしている
     * - メソッドの引数や戻り値を検証していない
     *
     * 改善方法:
     * メソッドを実際に呼び出して、APIリクエストやレスポンス処理を検証すべき
     */
    expect(typeof TodoService.createTodo).toBe("function");
  });
});
