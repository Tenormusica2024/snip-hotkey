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
3. F8 を押すと、画像が `snips` に保存され、ファイルパスが PowerShell に自動入力される（見えない場合は矢印キー入力などで再描画）。

## GitHub へアップするためにローカルへ取り込む手順（例）
1. リポジトリの作業ディレクトリへ移動（例: `C:\Users\B1443kouda\Documents\git\<repo>`）。
2. 必要ファイルをコピー:
   - `copy \"C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\snip_hotkey.py\" .`
   - `copy \"C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\README.md\" .`
   - `copy \"C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\snip_hotkey_spec.md\" .`
   - （必要なら `restart_snip_hotkey.cmd` もコピー）
3. Git で add/commit/push:
   - `git add snip_hotkey.py README.md snip_hotkey_spec.md restart_snip_hotkey.cmd`
   - `git commit -m \"Add snip_hotkey tool\"`
   - `git push`
