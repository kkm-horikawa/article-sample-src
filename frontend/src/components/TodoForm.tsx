/**
 * @fileoverview TODO作成フォームコンポーネント
 */

import type { Priority, TodoCreate } from "@/types";
import { useState } from "react";

/**
 * TODOフォームのプロパティ
 */
interface TodoFormProps {
	/** フォーム送信時のコールバック関数 */
	onSubmit: (todo: TodoCreate) => void;
	/** キャンセルボタン押下時のコールバック関数（オプション） */
	onCancel?: () => void;
}

/**
 * TODO作成フォームコンポーネント
 *
 * 新しいTODOを作成するためのフォームを表示します。
 * タイトル、説明、優先度、期限日を入力できます。
 *
 * @param {TodoFormProps} props - コンポーネントのプロパティ
 * @returns {JSX.Element} TODOフォーム
 */
export default function TodoForm({ onSubmit, onCancel }: TodoFormProps) {
	const [title, setTitle] = useState("");
	const [description, setDescription] = useState("");
	const [priority, setPriority] = useState<Priority>("medium");
	const [dueDate, setDueDate] = useState("");

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();

		if (!title.trim()) {
			alert("タイトルを入力してください");
			return;
		}

		onSubmit({
			title: title.trim(),
			description: description.trim(),
			priority,
			due_date: dueDate || null,
		});

		setTitle("");
		setDescription("");
		setPriority("medium");
		setDueDate("");
	};

	return (
		<form onSubmit={handleSubmit} className="todo-form">
			<div>
				<label htmlFor="title">タイトル *</label>
				<input
					type="text"
					id="title"
					value={title}
					onChange={(e) => setTitle(e.target.value)}
					maxLength={200}
					required
				/>
			</div>

			<div>
				<label htmlFor="description">説明</label>
				<textarea
					id="description"
					value={description}
					onChange={(e) => setDescription(e.target.value)}
					rows={3}
				/>
			</div>

			<div>
				<label htmlFor="priority">優先度</label>
				<select
					id="priority"
					value={priority}
					onChange={(e) => setPriority(e.target.value as Priority)}
				>
					<option value="low">低</option>
					<option value="medium">中</option>
					<option value="high">高</option>
				</select>
			</div>

			<div>
				<label htmlFor="due_date">期限</label>
				<input
					type="date"
					id="due_date"
					value={dueDate}
					onChange={(e) => setDueDate(e.target.value)}
				/>
			</div>

			<div className="form-actions">
				<button type="submit">作成</button>
				{onCancel && (
					<button type="button" onClick={onCancel}>
						キャンセル
					</button>
				)}
			</div>
		</form>
	);
}
