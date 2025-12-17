# snip_hotkey

Snipping Tool でコピーした画像を PNG に保存し、そのパス（引用符付き）をアクティブな PowerShell（Codex CLI）に自動入力する Windows 用ユーティリティ。

- ホットキー: F8（グローバル）
- 保存先: `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\snips`
- ログ: `snip_hotkey.log`（同ディレクトリ）
- 画像取得は 0.1 秒刻みで最大 5 回リトライしてから保存
- 入力するパスは `"C:\path\to\file.png"` のように引用符付きで送信
- 詳細仕様: `snip_hotkey_spec.md`

## 起動・再起動
- 自動起動: スタートアップの `snip_hotkey_start.cmd` で最小化 PowerShell から `py snip_hotkey.py` を起動。
- 手動再起動: `restart_snip_hotkey.cmd` をダブルクリック（ウィンドウタイトルが `snip_hotkey` の PowerShell だけを止めて再起動）。

## 使い方
1. Snipping Tool などで画像をコピー。
2. Codex CLI の PowerShell をフォーカス。
3. F8 を押すと、画像が `snips` に保存され、ファイルパスが PowerShell に自動入力される（見えない場合は矢印キー入力などで再描画）。***
