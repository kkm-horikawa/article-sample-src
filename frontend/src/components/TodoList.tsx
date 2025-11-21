/**
 * @fileoverview TODOリスト表示コンポーネント
 */

import type { Todo } from "@/types";
import TodoItem from "./TodoItem";

/**
 * TODOリストのプロパティ
 */
interface TodoListProps {
	/** 表示するTODOの配列 */
	todos: Todo[];
	/** 完了状態切り替え時のコールバック関数 */
	onToggle: (id: number) => void;
	/** 削除時のコールバック関数 */
	onDelete: (id: number) => void;
}

/**
 * TODOリスト表示コンポーネント
 *
 * TODOの配列を受け取り、TodoItemコンポーネントを使用して
 * リスト形式で表示します。TODOが0件の場合は空状態メッセージを表示します。
 *
 * @param {TodoListProps} props - コンポーネントのプロパティ
 * @returns {JSX.Element} TODOリストまたは空状態メッセージ
 */
export default function TodoList({ todos, onToggle, onDelete }: TodoListProps) {
	if (todos.length === 0) {
		return (
			<div className="empty-state" data-testid="empty-state">
				<p>TODOがありません</p>
			</div>
		);
	}

	return (
		<div className="todo-list" data-testid="todo-list">
			{todos.map((todo) => (
				<TodoItem
					key={todo.id}
					todo={todo}
					onToggle={onToggle}
					onDelete={onDelete}
				/>
			))}
		</div>
	);
}
