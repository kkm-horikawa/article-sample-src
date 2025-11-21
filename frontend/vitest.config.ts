/**
 * @fileoverview Vitest テストランナーの設定ファイル
 *
 * React コンポーネントとサービスのユニットテスト環境を定義します。
 * - React プラグインの有効化
 * - jsdom 環境でのテスト実行
 * - グローバルテスト API の有効化（describe, it, expect など）
 * - テストセットアップファイルの自動読み込み
 * - カバレッジレポートの設定（v8 プロバイダー）
 * - パスエイリアス（@）の設定
 */

import path from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
	/** React プラグインを有効化 */
	plugins: [react()],
	/** テスト実行の設定 */
	test: {
		/** グローバルテスト API を有効化（describe, it, expect など） */
		globals: true,
		/** ブラウザ環境をシミュレートする jsdom を使用 */
		environment: "jsdom",
		/** テスト実行前に自動的にロードするセットアップファイル */
		setupFiles: "./tests/setup/setupTests.ts",
		/** テストファイルのパターン */
		include: ["tests/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
		/** カバレッジレポートの設定 */
		coverage: {
			/** v8 カバレッジプロバイダーを使用 */
			provider: "v8",
			/** レポート形式（テキスト、JSON、HTML） */
			reporter: ["text", "json", "html"],
			/** カバレッジ計測から除外するパス */
			exclude: [
				"node_modules/",
				"tests/",
				"**/*.config.ts",
				"**/*.d.ts",
				"**/types/",
			],
		},
	},
	/** モジュール解決の設定 */
	resolve: {
		/** パスエイリアス（@ を src ディレクトリにマッピング） */
		alias: {
			"@": path.resolve(__dirname, "./src"),
		},
	},
});
