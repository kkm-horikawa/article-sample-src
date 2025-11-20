/**
 * @fileoverview アプリケーションのエントリーポイント
 *
 * React アプリケーションを DOM にマウントし、StrictMode で実行します。
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

/** アプリケーションのルート要素（index.html の #root） */
const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Root element not found");
}

/**
 * React アプリケーションを DOM にマウント
 * StrictMode で開発時の潜在的な問題を検出します
 */
createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
