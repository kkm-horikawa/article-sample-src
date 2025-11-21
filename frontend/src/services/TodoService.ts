/**
 * @fileoverview TODO API通信サービス
 */

import type {
	Priority,
	Todo,
	TodoCreate,
	TodoStatistics,
	TodoUpdate,
} from "@/types";

/** API のベースURL */
const API_BASE_URL =
	import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

/**
 * TODO API通信サービスクラス
 *
 * バックエンドのTODO APIとの通信を担当するサービスクラスです。
 * CRUD操作、完了状態の切り替え、一括削除、統計情報取得などの
 * すべてのAPI呼び出しをカプセル化します。
 */
class TodoService {
	/**
	 * APIリクエストを実行する共通メソッド
	 *
	 * @template T - レスポンスの型
	 * @param {string} endpoint - APIエンドポイント
	 * @param {RequestInit} [options] - fetchオプション
	 * @returns {Promise<T>} API レスポンス
	 * @throws {Error} HTTPエラーまたはネットワークエラー
	 */
	private async request<T>(
		endpoint: string,
		options?: RequestInit,
	): Promise<T> {
		const response = await fetch(`${API_BASE_URL}${endpoint}`, {
			headers: {
				"Content-Type": "application/json",
				...options?.headers,
			},
			...options,
		});

		if (!response.ok) {
			const error = await response.json().catch(() => ({}));
			throw new Error(error.detail || `HTTP error! status: ${response.status}`);
		}

		// Handle empty responses (e.g., 204 No Content for DELETE)
		const text = await response.text();
		return text ? JSON.parse(text) : ({} as T);
	}

	/**
	 * TODO一覧を取得する
	 *
	 * @param {object} [params] - フィルタパラメータ
	 * @param {boolean} [params.completed] - 完了状態でフィルタ
	 * @param {Priority} [params.priority] - 優先度でフィルタ
	 * @param {boolean} [params.overdue_only] - 期限切れのみ取得
	 * @returns {Promise<Todo[]>} TODO の配列
	 */
	async getTodos(params?: {
		completed?: boolean;
		priority?: Priority;
		overdue_only?: boolean;
	}): Promise<Todo[]> {
		const queryParams = new URLSearchParams();

		if (params?.completed !== undefined) {
			queryParams.append("completed", String(params.completed));
		}
		if (params?.priority) {
			queryParams.append("priority", params.priority);
		}
		if (params?.overdue_only) {
			queryParams.append("overdue_only", "true");
		}

		const query = queryParams.toString();
		const endpoint = query ? `/todos/?${query}` : "/todos/";

		const response = await this.request<{ results: Todo[] }>(endpoint);
		return response.results;
	}

	/**
	 * 指定したIDのTODOを取得する
	 *
	 * @param {number} id - TODO ID
	 * @returns {Promise<Todo>} TODO オブジェクト
	 */
	async getTodo(id: number): Promise<Todo> {
		return this.request<Todo>(`/todos/${id}/`);
	}

	/**
	 * 新しいTODOを作成する
	 *
	 * @param {TodoCreate} data - 作成するTODOのデータ
	 * @returns {Promise<Todo>} 作成されたTODOオブジェクト
	 */
	async createTodo(data: TodoCreate): Promise<Todo> {
		return this.request<Todo>("/todos/", {
			method: "POST",
			body: JSON.stringify(data),
		});
	}

	/**
	 * 既存のTODOを更新する
	 *
	 * @param {number} id - 更新するTODOのID
	 * @param {TodoUpdate} data - 更新するデータ
	 * @returns {Promise<Todo>} 更新されたTODOオブジェクト
	 */
	async updateTodo(id: number, data: TodoUpdate): Promise<Todo> {
		return this.request<Todo>(`/todos/${id}/`, {
			method: "PATCH",
			body: JSON.stringify(data),
		});
	}

	/**
	 * 指定したIDのTODOを削除する
	 *
	 * @param {number} id - 削除するTODOのID
	 * @returns {Promise<void>}
	 */
	async deleteTodo(id: number): Promise<void> {
		await this.request<void>(`/todos/${id}/`, {
			method: "DELETE",
		});
	}

	/**
	 * 指定したIDのTODOの完了状態を切り替える
	 *
	 * @param {number} id - 切り替えるTODOのID
	 * @returns {Promise<Todo>} 更新されたTODOオブジェクト
	 */
	async toggleTodo(id: number): Promise<Todo> {
		return this.request<Todo>(`/todos/${id}/toggle/`, {
			method: "POST",
		});
	}

	/**
	 * 完了済みのTODOを一括削除する
	 *
	 * @returns {Promise<{deleted_count: number}>} 削除件数
	 */
	async bulkDeleteCompleted(): Promise<{ deleted_count: number }> {
		return this.request<{ deleted_count: number }>(
			"/todos/bulk_delete_completed/",
			{
				method: "DELETE",
			},
		);
	}

	/**
	 * TODO統計情報を取得する
	 *
	 * @returns {Promise<TodoStatistics>} 統計情報（全体件数、完了件数、未完了件数、期限切れ件数）
	 */
	async getStatistics(): Promise<TodoStatistics> {
		return this.request<TodoStatistics>("/todos/statistics/");
	}
}

export default new TodoService();
