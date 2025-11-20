/**
 * @fileoverview TodoItemコンポーネントのテスト
 *
 * このファイルは、TodoItemコンポーネントの各種機能をテストします。
 * 良いテスト例、悪いテスト例、優先度の低いテスト例に分類しています。
 */

import TodoItem from "@/components/TodoItem";
import type { Todo } from "@/types";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

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

describe("TodoItem - Good Examples", () => {
  it("renders todo information correctly", () => {
    /**
     * TODO情報が正しくレンダリングされることを確認する
     *
     * 【テストの意図】TodoItemコンポーネントがTODOの全情報を正しく表示することを保証します。
     * 【何を保証するか】タイトル、説明、優先度、期限が表示されること
     * 【テスト手順】mockTodoをレンダリング→各要素がDOMに存在することを検証
     * 【期待する結果】すべての情報が表示されること
     */
    render(<TodoItem todo={mockTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.getByText("Test TODO")).toBeInTheDocument();
    expect(screen.getByText("Test Description")).toBeInTheDocument();
    expect(screen.getByText("中")).toBeInTheDocument();
    expect(screen.getByText(/2025\/12\/31/)).toBeInTheDocument();
  });

  it("calls onToggle when checkbox is clicked", async () => {
    /**
     * チェックボックスクリック時にonToggleが呼ばれることを確認する
     *
     * 【テストの意図】ユーザーがチェックボックスをクリックした時、onToggleコールバックが正しく呼ばれることを保証します。
     * 【何を保証するか】onToggleが正しいID(1)で呼ばれること
     * 【テスト手順】コンポーネントをレンダリング→チェックボックスをクリック→onToggleの呼び出しを検証
     * 【期待する結果】onToggleがID=1で1回呼ばれること
     */
    const onToggle = vi.fn();
    const user = userEvent.setup();

    render(<TodoItem todo={mockTodo} onToggle={onToggle} onDelete={vi.fn()} />);

    const checkbox = screen.getByRole("checkbox");
    await user.click(checkbox);

    expect(onToggle).toHaveBeenCalledWith(1);
  });

  it("calls onDelete when delete button is clicked", async () => {
    /**
     * 削除ボタンクリック時にonDeleteが呼ばれることを確認する
     *
     * 【テストの意図】ユーザーが削除ボタンをクリックした時、onDeleteコールバックが正しく呼ばれることを保証します。
     * 【何を保証するか】onDeleteが正しいID(1)で呼ばれること
     * 【テスト手順】コンポーネントをレンダリング→削除ボタンをクリック→onDeleteの呼び出しを検証
     * 【期待する結果】onDeleteがID=1で1回呼ばれること
     */
    const onDelete = vi.fn();
    const user = userEvent.setup();

    render(<TodoItem todo={mockTodo} onToggle={vi.fn()} onDelete={onDelete} />);

    await user.click(screen.getByRole("button", { name: /削除/i }));

    expect(onDelete).toHaveBeenCalledWith(1);
  });

  it("applies completed style when todo is completed", () => {
    /**
     * 完了TODOに完了スタイルが適用されることを確認する
     *
     * 【テストの意図】完了状態のTODOに"completed"クラスが適用され、視覚的に区別できることを保証します。
     * 【何を保証するか】completedがtrueの時、todo-item要素に"completed"クラスが追加されること
     * 【テスト手順】完了TODOをレンダリング→todo-item要素のクラスを検証
     * 【期待する結果】todo-item要素に"completed"クラスが含まれること
     */
    const completedTodo = { ...mockTodo, completed: true };

    render(<TodoItem todo={completedTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);

    const todoItem = screen.getByTestId("todo-item");
    expect(todoItem).toHaveClass("completed");
  });

  it("shows overdue style when todo is overdue", () => {
    /**
     * 期限切れTODOに期限切れスタイルが適用されることを確認する
     *
     * 【テストの意図】期限切れのTODOに"overdue"クラスが適用され、視覚的に警告できることを保証します。
     * 【何を保証するか】is_overdueがtrueの時、期限表示要素に"overdue"クラスが追加されること
     * 【テスト手順】期限切れTODOをレンダリング→期限表示要素のクラスを検証
     * 【期待する結果】期限表示要素に"overdue"クラスが含まれること
     */
    const overdueTodo = { ...mockTodo, is_overdue: true };

    render(<TodoItem todo={overdueTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);

    const dueDate = screen.getByText(/期限:/);
    expect(dueDate).toHaveClass("overdue");
  });

  it("does not render description when empty", () => {
    /**
     * 説明が空の場合、説明欄がレンダリングされないことを確認する
     *
     * 【テストの意図】説明が空文字列の場合、無駄なDOM要素を生成しないことを保証します。
     * 【何を保証するか】descriptionが空の時、説明要素がレンダリングされないこと
     * 【テスト手順】説明なしTODOをレンダリング→説明要素がDOMに存在しないことを検証
     * 【期待する結果】説明要素がDOMに存在しないこと
     */
    const noDescTodo = { ...mockTodo, description: "" };

    render(<TodoItem todo={noDescTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.queryByText("Test Description")).not.toBeInTheDocument();
  });

  it("does not render due date when null", () => {
    /**
     * 期限がnullの場合、期限欄がレンダリングされないことを確認する
     *
     * 【テストの意図】期限が設定されていない場合、無駄なDOM要素を生成しないことを保証します。
     * 【何を保証するか】due_dateがnullの時、期限要素がレンダリングされないこと
     * 【テスト手順】期限なしTODOをレンダリング→期限要素がDOMに存在しないことを検証
     * 【期待する結果】期限要素がDOMに存在しないこと
     */
    const noDueDateTodo = { ...mockTodo, due_date: null };

    render(<TodoItem todo={noDueDateTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);

    expect(screen.queryByText(/期限:/)).not.toBeInTheDocument();
  });

  it("applies correct priority class for high priority", () => {
    /**
     * 高優先度TODOに正しい優先度クラスが適用されることを確認する
     *
     * 【テストの意図】優先度に応じて正しいCSSクラスが適用され、視覚的に区別できることを保証します。
     * 【何を保証するか】priorityが"high"の時、優先度バッジに"priority-high"クラスが追加されること
     * 【テスト手順】高優先度TODOをレンダリング→優先度バッジ要素のクラスを検証
     * 【期待する結果】優先度バッジに"priority-high"クラスが含まれること
     */
    const highPriorityTodo = { ...mockTodo, priority: "high" as const, priority_display_ja: "高" };

    render(<TodoItem todo={highPriorityTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);

    const priorityBadge = screen.getByText("高");
    expect(priorityBadge).toHaveClass("priority-high");
  });

  it("checkbox is checked when todo is completed", () => {
    /**
     * 完了TODOのチェックボックスがチェック状態であることを確認する
     *
     * 【テストの意図】完了状態のTODOがチェックボックスでも正しく表示されることを保証します。
     * 【何を保証するか】completedがtrueの時、チェックボックスのchecked属性がtrueであること
     * 【テスト手順】完了TODOをレンダリング→チェックボックスのchecked属性を検証
     * 【期待する結果】チェックボックスのcheckedがtrueであること
     */
    const completedTodo = { ...mockTodo, completed: true };

    render(<TodoItem todo={completedTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);

    const checkbox = screen.getByRole("checkbox") as HTMLInputElement;
    expect(checkbox.checked).toBe(true);
  });
});

describe("TodoItem - Bad Examples", () => {
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
      <TodoItem todo={mockTodo} onToggle={vi.fn()} onDelete={vi.fn()} />,
    );
    expect(container.firstChild).toBeTruthy();
  });
});

describe("TodoItem - Low Priority Examples", () => {
  it("has todo-item data-testid", () => {
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
    render(<TodoItem todo={mockTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);
    expect(screen.getByTestId("todo-item")).toBeInTheDocument();
  });

  it("delete button has correct class", () => {
    /**
     * 【優先度低】削除ボタンのクラス名をチェックする
     *
     * このテストの優先度が低い理由:
     * - CSSクラス名は実装の詳細に依存している
     * - クラス名の変更でテストが壊れる保守性の問題がある
     * - ボタンの機能ではなくスタイリングをテストしている
     *
     * 改善方法:
     * ボタンのクリック動作やaria属性など、ユーザーに影響する部分をテストすべき
     */
    render(<TodoItem todo={mockTodo} onToggle={vi.fn()} onDelete={vi.fn()} />);
    const deleteButton = screen.getByRole("button", { name: /削除/i });
    expect(deleteButton).toHaveClass("delete-btn");
  });
});
