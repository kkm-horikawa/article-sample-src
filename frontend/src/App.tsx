/**
 * @fileoverview TODO アプリケーションのメインコンポーネント
 */

import TodoForm from "@/components/TodoForm";
import TodoList from "@/components/TodoList";
import TodoService from "@/services/TodoService";
import type { Priority, Todo, TodoCreate } from "@/types";
import { useEffect, useState } from "react";

/**
 * TODO アプリケーションのルートコンポーネント
 *
 * TODO の作成、表示、更新、削除、フィルタリング機能を提供します。
 * 状態管理とバックエンド API との通信を統括します。
 *
 * @returns {JSX.Element} TODO アプリケーションの UI
 */
function App() {
  /** TODO 一覧の状態 */
  const [todos, setTodos] = useState<Todo[]>([]);
  /** ローディング状態 */
  const [loading, setLoading] = useState(true);
  /** エラーメッセージの状態 */
  const [error, setError] = useState<string | null>(null);
  /** 完了状態フィルタ（すべて / 未完了 / 完了） */
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");
  /** 優先度フィルタ（すべて / 低 / 中 / 高） */
  const [priorityFilter, setPriorityFilter] = useState<Priority | "all">("all");

  /**
   * TODO 一覧を取得する
   *
   * フィルタ条件に基づいて API から TODO を取得し、状態を更新します。
   * エラーが発生した場合はエラーメッセージを設定します。
   */
  const fetchTodos = async () => {
    try {
      setLoading(true);
      const params: {
        completed?: boolean;
        priority?: Priority;
      } = {};

      // フィルタ条件に応じてパラメータを設定
      if (filter === "active") params.completed = false;
      if (filter === "completed") params.completed = true;
      if (priorityFilter !== "all") params.priority = priorityFilter;

      const data = await TodoService.getTodos(params);
      setTodos(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  /**
   * フィルタ条件変更時の副作用
   *
   * filter または priorityFilter が変更されたら TODO 一覧を再取得します。
   * 初回マウント時にも実行されます。
   */
  useEffect(() => {
    fetchTodos();
  }, [filter, priorityFilter]);

  /**
   * 新しい TODO を作成するハンドラ
   *
   * @param {TodoCreate} data - 作成する TODO のデータ
   */
  const handleCreate = async (data: TodoCreate) => {
    try {
      await TodoService.createTodo(data);
      await fetchTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "作成に失敗しました");
    }
  };

  /**
   * TODO の完了状態を切り替えるハンドラ
   *
   * @param {number} id - 切り替える TODO の ID
   */
  const handleToggle = async (id: number) => {
    try {
      await TodoService.toggleTodo(id);
      await fetchTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "更新に失敗しました");
    }
  };

  /**
   * TODO を削除するハンドラ
   *
   * ユーザーに確認ダイアログを表示してから削除を実行します。
   *
   * @param {number} id - 削除する TODO の ID
   */
  const handleDelete = async (id: number) => {
    if (!window.confirm("このTODOを削除しますか？")) return;

    try {
      await TodoService.deleteTodo(id);
      await fetchTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "削除に失敗しました");
    }
  };

  /**
   * 完了済みの TODO を一括削除するハンドラ
   *
   * ユーザーに確認ダイアログを表示してから一括削除を実行します。
   */
  const handleBulkDelete = async () => {
    if (!window.confirm("完了済みのTODOをすべて削除しますか？")) return;

    try {
      await TodoService.bulkDeleteCompleted();
      await fetchTodos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "削除に失敗しました");
    }
  };

  if (loading) {
    return <div>読み込み中...</div>;
  }

  return (
    <div className="app">
      <header>
        <h1>TODO App</h1>
      </header>

      <main>
        {error && <div className="error">{error}</div>}

        <section className="todo-form-section">
          <h2>新しいTODO</h2>
          <TodoForm onSubmit={handleCreate} />
        </section>

        <section className="todo-list-section">
          <div className="filters">
            <div>
              <label htmlFor="filter">フィルタ:</label>
              <select
                id="filter"
                value={filter}
                onChange={(e) => setFilter(e.target.value as typeof filter)}
              >
                <option value="all">すべて</option>
                <option value="active">未完了</option>
                <option value="completed">完了</option>
              </select>
            </div>

            <div>
              <label htmlFor="priority-filter">優先度:</label>
              <select
                id="priority-filter"
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value as typeof priorityFilter)}
              >
                <option value="all">すべて</option>
                <option value="low">低</option>
                <option value="medium">中</option>
                <option value="high">高</option>
              </select>
            </div>

            <button type="button" onClick={handleBulkDelete}>
              完了済みを削除
            </button>
          </div>

          <TodoList todos={todos} onToggle={handleToggle} onDelete={handleDelete} />
        </section>
      </main>
    </div>
  );
}

export default App;
