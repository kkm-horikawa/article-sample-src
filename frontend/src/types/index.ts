/**
 * @fileoverview TODO アプリケーションで使用する型定義
 */

/**
 * TODO の優先度
 *
 * - low: 低優先度
 * - medium: 中優先度
 * - high: 高優先度
 */
export type Priority = "low" | "medium" | "high";

/**
 * TODO オブジェクトの型定義
 *
 * バックエンド API から取得される TODO の完全な情報を表します。
 */
export interface Todo {
  /** TODO の一意識別子 */
  id: number;
  /** TODO のタイトル */
  title: string;
  /** TODO の詳細説明 */
  description: string;
  /** 完了状態（true: 完了、false: 未完了） */
  completed: boolean;
  /** 優先度 */
  priority: Priority;
  /** 優先度の日本語表示名 */
  priority_display_ja: string;
  /** 期限日（ISO 8601 形式の文字列、または null） */
  due_date: string | null;
  /** 期限切れかどうか */
  is_overdue: boolean;
  /** 作成日時（ISO 8601 形式の文字列） */
  created_at: string;
  /** 更新日時（ISO 8601 形式の文字列） */
  updated_at: string;
}

/**
 * TODO 作成時のリクエストデータ型定義
 *
 * 新しい TODO を作成する際に API に送信するデータの形式です。
 */
export interface TodoCreate {
  /** TODO のタイトル（必須） */
  title: string;
  /** TODO の詳細説明（任意） */
  description?: string;
  /** 優先度（任意、デフォルト: medium） */
  priority?: Priority;
  /** 期限日（任意） */
  due_date?: string | null;
}

/**
 * TODO 更新時のリクエストデータ型定義
 *
 * 既存の TODO を更新する際に API に送信するデータの形式です。
 * すべてのフィールドが任意であり、指定されたフィールドのみが更新されます。
 */
export interface TodoUpdate {
  /** TODO のタイトル */
  title?: string;
  /** TODO の詳細説明 */
  description?: string;
  /** 完了状態 */
  completed?: boolean;
  /** 優先度 */
  priority?: Priority;
  /** 期限日 */
  due_date?: string | null;
}

/**
 * TODO 統計情報の型定義
 *
 * TODO の集計データを表します。
 */
export interface TodoStatistics {
  /** 全体の TODO 件数 */
  total: number;
  /** 完了済みの TODO 件数 */
  completed: number;
  /** 未完了の TODO 件数 */
  pending: number;
  /** 期限切れの TODO 件数 */
  overdue: number;
}
