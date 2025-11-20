/**
 * @fileoverview Vite ビルドツールの設定ファイル
 *
 * React アプリケーションのビルドと開発サーバーの設定を定義します。
 * - React プラグインの有効化
 * - パスエイリアス（@）の設定
 * - 開発サーバーのポートとホスト設定
 */

import react from "@vitejs/plugin-react";
import path from "path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    host: true,
  },
});
