/**
 * @fileoverview TodoListコンポーネントのテスト
 *
 * このファイルは、TodoListコンポーネントの各種機能をテストします。
 * 良いテスト例、悪いテスト例、優先度の低いテスト例に分類しています。
 */

import TodoList from "@/components/TodoList";
import type { Todo } from "@/types";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

/** テスト用のモックTODO配列 */
const mockTodos: Todo[] = [
	{
		id: 1,
		title: "First TODO",
		description: "First Description",
		completed: false,
		priority: "high",
		priority_display_ja: "高",
		due_date: "2025-12-31",
		is_overdue: false,
		created_at: "2025-11-20T10:00:00Z",
		updated_at: "2025-11-20T10:00:00Z",
	},
	{
		id: 2,
		title: "Second TODO",
		description: "Second Description",
		completed: true,
		priority: "low",
		priority_display_ja: "低",
		due_date: null,
		is_overdue: false,
		created_at: "2025-11-20T11:00:00Z",
		updated_at: "2025-11-20T11:00:00Z",
	},
];

describe("TodoList - Good Examples", () => {
	it("renders all todos", () => {
		/**
		 * すべてのTODOがレンダリングされることを確認する
		 *
		 * 【テストの意図】TodoListコンポーネントが渡されたすべてのTODOを表示することを保証します。
		 * 【何を保証するか】配列内のすべてのTODOのタイトルが表示されること
		 * 【テスト手順】2件のTODOをレンダリング→各TODOのタイトルがDOMに存在することを検証
		 * 【期待する結果】すべてのTODOのタイトルが表示されること
		 */
		render(
			<TodoList todos={mockTodos} onToggle={vi.fn()} onDelete={vi.fn()} />,
		);

		expect(screen.getByText("First TODO")).toBeInTheDocument();
		expect(screen.getByText("Second TODO")).toBeInTheDocument();
	});

	it("renders empty state when no todos", () => {
		/**
		 * TODOが0件の時に空状態メッセージが表示されることを確認する
		 *
		 * 【テストの意図】TodoListコンポーネントがTODOが0件の場合に適切な空状態メッセージを表示することを保証します。
		 * 【何を保証するか】空配列の時に「TODOがありません」メッセージと空状態要素が表示されること
		 * 【テスト手順】空配列をレンダリング→空状態メッセージと要素を検証
		 * 【期待する結果】空状態メッセージとempty-state要素が表示されること
		 */
		render(<TodoList todos={[]} onToggle={vi.fn()} onDelete={vi.fn()} />);

		expect(screen.getByText("TODOがありません")).toBeInTheDocument();
		expect(screen.getByTestId("empty-state")).toBeInTheDocument();
	});

	it("renders correct number of todo items", () => {
		/**
		 * 正しい件数のTODOアイテムがレンダリングされることを確認する
		 *
		 * 【テストの意図】TodoListコンポーネントが配列の長さに応じて正しい件数のTodoItemをレンダリングすることを保証します。
		 * 【何を保証するか】配列の長さと表示されるTODOアイテムの数が一致すること
		 * 【テスト手順】2件のTODOをレンダリング→todo-item要素の数を検証
		 * 【期待する結果】todo-item要素が2つ存在すること
		 */
		render(
			<TodoList todos={mockTodos} onToggle={vi.fn()} onDelete={vi.fn()} />,
		);

		const todoItems = screen.getAllByTestId("todo-item");
		expect(todoItems).toHaveLength(2);
	});

	it("passes callbacks to TodoItem components", () => {
		/**
		 * コールバック関数が子コンポーネントに正しく渡されることを確認する
		 *
		 * 【テストの意図】TodoListコンポーネントがonToggleとonDeleteを各TodoItemに正しく渡すことを保証します。
		 * 【何を保証するか】各TODOにチェックボックスと削除ボタンが存在すること
		 * 【テスト手順】2件のTODOをレンダリング→チェックボックスと削除ボタンの数を検証
		 * 【期待する結果】チェックボックスと削除ボタンがそれぞれ2つ存在すること
		 */
		const onToggle = vi.fn();
		const onDelete = vi.fn();

		render(
			<TodoList todos={mockTodos} onToggle={onToggle} onDelete={onDelete} />,
		);

		expect(screen.getAllByRole("checkbox")).toHaveLength(2);
		expect(screen.getAllByRole("button", { name: /削除/i })).toHaveLength(2);
	});
});

describe("TodoList - Bad Examples", () => {
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
		 * 実際のコンポーネントの動作や状態を検証すべき
		 */
		expect(true).toBe(true);
	});

	it("checks if component renders", () => {
		/**
		 * 【悪い例】コンポーネントがレンダリングされるかをチェックする
		 *
		 * このテストが悪い理由:
		 * - firstChildがtruthyであることしか検証していない
		 * - Reactフレームワークの責任範囲をテストしている
		 * - 具体的な要素や動作を検証していない
		 *
		 * 改善方法:
		 * 特定のテキストや要素の存在を検証すべき
		 */
		const { container } = render(
			<TodoList todos={mockTodos} onToggle={vi.fn()} onDelete={vi.fn()} />,
		);
		expect(container.firstChild).toBeTruthy();
	});
});

describe("TodoList - Low Priority Examples", () => {
	it("has todo-list data-testid when todos exist", () => {
		/**
		 * 【優先度低】data-testid属性の存在をチェックする
		 *
		 * このテストの優先度が低い理由:
		 * - data-testid は実装の詳細に依存している
		 * - ユーザーには見えない属性をテストしている
		 * - 実際の機能や動作を保証していない
		 *
		 * ただし、以下の場合は有用:
		 * - E2Eテストで要素を特定する必要がある場合
		 * - テスト用の一意な識別子が必要な場合
		 */
		render(
			<TodoList todos={mockTodos} onToggle={vi.fn()} onDelete={vi.fn()} />,
		);
		expect(screen.getByTestId("todo-list")).toBeInTheDocument();
	});

	it("uses key prop for todo items", () => {
		/**
		 * 【優先度低】TODOアイテムがkey propを使用しているかチェックする
		 *
		 * このテストの優先度が低い理由:
		 * - Reactのkey propは開発モードで警告が出るため、テストで検証する必要性が低い
		 * - CSSクラス名でDOM要素を検索しており、実装の詳細に依存している
		 * - keyの存在ではなく、レンダリングされた要素の数を検証している
		 *
		 * 改善方法:
		 * 実際のユーザーに影響する機能や動作をテストすべき
		 */
		const { container } = render(
			<TodoList todos={mockTodos} onToggle={vi.fn()} onDelete={vi.fn()} />,
		);
		expect(container.querySelectorAll(".todo-item")).toHaveLength(2);
	});
});
