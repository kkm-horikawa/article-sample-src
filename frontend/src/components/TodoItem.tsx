/**
 * @fileoverview TODO項目表示コンポーネント
 */

import type { Todo } from "@/types";
import { format } from "date-fns";

/**
 * TODOアイテムのプロパティ
 */
interface TodoItemProps {
	/** 表示するTODOオブジェクト */
	todo: Todo;
	/** 完了状態切り替え時のコールバック関数 */
	onToggle: (id: number) => void;
	/** 削除時のコールバック関数 */
	onDelete: (id: number) => void;
}

/**
 * TODO項目表示コンポーネント
 *
 * 個別のTODOアイテムを表示し、完了チェックボックス、優先度バッジ、
 * 期限表示、削除ボタンなどを提供します。
 *
 * @param {TodoItemProps} props - コンポーネントのプロパティ
 * @returns {JSX.Element} TODOアイテム
 */
export default function TodoItem({ todo, onToggle, onDelete }: TodoItemProps) {
	/**
	 * 優先度に応じたCSSクラス名を取得する
	 *
	 * @param {string} priority - 優先度 ("high" | "medium" | "low")
	 * @returns {string} CSSクラス名
	 */
	const getPriorityClass = (priority: string) => {
		switch (priority) {
			case "high":
				return "priority-high";
			case "medium":
				return "priority-medium";
			case "low":
				return "priority-low";
			default:
				return "";
		}
	};

	return (
		<div
			className={`todo-item ${todo.completed ? "completed" : ""}`}
			data-testid="todo-item"
		>
			<div className="todo-checkbox">
				<input
					type="checkbox"
					checked={todo.completed}
					onChange={() => onToggle(todo.id)}
					aria-label={`${todo.title}を完了する`}
				/>
			</div>

			<div className="todo-content">
				<h3 className="todo-title">{todo.title}</h3>
				{todo.description && (
					<p className="todo-description">{todo.description}</p>
				)}

				<div className="todo-meta">
					<span className={`priority-badge ${getPriorityClass(todo.priority)}`}>
						{todo.priority_display_ja}
					</span>

					{todo.due_date && (
						<span className={`due-date ${todo.is_overdue ? "overdue" : ""}`}>
							期限: {format(new Date(todo.due_date), "yyyy/MM/dd")}
						</span>
					)}

					<span className="created-at">
						作成: {format(new Date(todo.created_at), "yyyy/MM/dd HH:mm")}
					</span>
				</div>
			</div>

			<div className="todo-actions">
				<button
					type="button"
					onClick={() => onDelete(todo.id)}
					className="delete-btn"
				>
					削除
				</button>
			</div>
		</div>
	);
}
