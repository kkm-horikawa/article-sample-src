/**
 * @fileoverview TodoFormコンポーネントのテスト
 *
 * このファイルは、TodoFormコンポーネントの各種機能をテストします。
 * 良いテスト例、悪いテスト例、優先度の低いテスト例に分類しています。
 */

import TodoForm from "@/components/TodoForm";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

describe("TodoForm - Good Examples", () => {
	it("renders all form fields", () => {
		/**
		 * フォームの全フィールドがレンダリングされることを確認する
		 *
		 * 【テストの意図】
		 * フォームコンポーネントが必要なすべてのフィールドを表示することを保証します。
		 *
		 * 【何を保証するか】
		 * - タイトル入力フィールドが表示されること
		 * - 説明入力フィールドが表示されること
		 * - 優先度選択フィールドが表示されること
		 * - 期限日入力フィールドが表示されること
		 * - 作成ボタンが表示されること
		 *
		 * 【テスト手順】
		 * 1. TodoFormコンポーネントをレンダリング
		 * 2. 各フィールドとボタンがDOMに存在することを確認
		 *
		 * 【期待する結果】
		 * すべてのフィールドとボタンがDOMに存在する
		 */
		render(<TodoForm onSubmit={vi.fn()} />);

		expect(screen.getByLabelText(/タイトル/i)).toBeInTheDocument();
		expect(screen.getByLabelText(/説明/i)).toBeInTheDocument();
		expect(screen.getByLabelText(/優先度/i)).toBeInTheDocument();
		expect(screen.getByLabelText(/期限/i)).toBeInTheDocument();
		expect(screen.getByRole("button", { name: /作成/i })).toBeInTheDocument();
	});

	it("submits form with valid data", async () => {
		const onSubmit = vi.fn();
		const user = userEvent.setup();

		render(<TodoForm onSubmit={onSubmit} />);

		await user.type(screen.getByLabelText(/タイトル/i), "New TODO");
		await user.type(screen.getByLabelText(/説明/i), "Description");
		await user.selectOptions(screen.getByLabelText(/優先度/i), "high");

		await user.click(screen.getByRole("button", { name: /作成/i }));

		expect(onSubmit).toHaveBeenCalledWith({
			title: "New TODO",
			description: "Description",
			priority: "high",
			due_date: null,
		});
	});

	it("shows alert when submitting whitespace-only title", async () => {
		const onSubmit = vi.fn();
		const user = userEvent.setup();
		const alertSpy = vi.spyOn(window, "alert").mockImplementation(() => {});

		render(<TodoForm onSubmit={onSubmit} />);

		await user.type(screen.getByLabelText(/タイトル/i), "   ");
		await user.click(screen.getByRole("button", { name: /作成/i }));

		expect(alertSpy).toHaveBeenCalledWith("タイトルを入力してください");
		expect(onSubmit).not.toHaveBeenCalled();

		alertSpy.mockRestore();
	});

	it("trims whitespace from title and description", async () => {
		const onSubmit = vi.fn();
		const user = userEvent.setup();

		render(<TodoForm onSubmit={onSubmit} />);

		await user.type(screen.getByLabelText(/タイトル/i), "  Trimmed  ");
		await user.type(screen.getByLabelText(/説明/i), "  Description  ");
		await user.click(screen.getByRole("button", { name: /作成/i }));

		expect(onSubmit).toHaveBeenCalledWith({
			title: "Trimmed",
			description: "Description",
			priority: "medium",
			due_date: null,
		});
	});

	it("resets form after successful submission", async () => {
		const onSubmit = vi.fn();
		const user = userEvent.setup();

		render(<TodoForm onSubmit={onSubmit} />);

		const titleInput = screen.getByLabelText(/タイトル/i) as HTMLInputElement;
		const descInput = screen.getByLabelText(/説明/i) as HTMLTextAreaElement;

		await user.type(titleInput, "Test TODO");
		await user.type(descInput, "Test Description");
		await user.click(screen.getByRole("button", { name: /作成/i }));

		expect(titleInput.value).toBe("");
		expect(descInput.value).toBe("");
	});

	it("calls onCancel when cancel button is clicked", async () => {
		const onCancel = vi.fn();
		const user = userEvent.setup();

		render(<TodoForm onSubmit={vi.fn()} onCancel={onCancel} />);

		await user.click(screen.getByRole("button", { name: /キャンセル/i }));

		expect(onCancel).toHaveBeenCalled();
	});

	it("does not render cancel button when onCancel is not provided", () => {
		render(<TodoForm onSubmit={vi.fn()} />);

		expect(
			screen.queryByRole("button", { name: /キャンセル/i }),
		).not.toBeInTheDocument();
	});
});

describe("TodoForm - Bad Examples", () => {
	it("always passes", () => {
		expect(true).toBe(true);
	});

	it("checks component instance", () => {
		const { container } = render(<TodoForm onSubmit={vi.fn()} />);
		expect(container.querySelector(".todo-form")).toBeTruthy();
	});
});

describe("TodoForm - Low Priority Examples", () => {
	it("has correct form class name", () => {
		const { container } = render(<TodoForm onSubmit={vi.fn()} />);
		expect(container.querySelector("form")).toHaveClass("todo-form");
	});

	it("title input has maxLength attribute", () => {
		render(<TodoForm onSubmit={vi.fn()} />);
		const titleInput = screen.getByLabelText(/タイトル/i);
		expect(titleInput).toHaveAttribute("maxLength", "200");
	});
});
