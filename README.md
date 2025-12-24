# snip_hotkey

Snipping Tool でコピーした画像を PNG に保存し、そのパス（引用符付き）をアクティブな PowerShell（Codex CLI）に自動入力する Windows 用ユーティリティ。

- ホットキー: F8（グローバル）
- 保存先: `C:\Users\{USERNAME}\Documents\snips`（環境変数 `SNIP_HOTKEY_SAVE_DIR` で変更可能）
- ログ: `snip_hotkey.log`（同ディレクトリ）
- 画像取得は 0.1 秒刻みで最大 5 回リトライしてから保存
- 入力するパスは `"C:\path\to\file.png"` のように引用符付きで送信
- 詳細仕様: `snip_hotkey_spec.md`
- ホットキー登録は Win32 `RegisterHotKey` を使用（長時間稼働でのフック切れを回避）

## 起動・再起動
- 自動起動: スタートアップの `snip_hotkey_start.cmd` で非表示（pythonw）起動。
- 手動再起動: `restart_snip_hotkey.cmd` をダブルクリック（既存の `snip_hotkey.py` プロセスを落として pythonw で非表示再起動）。

## 使い方
1. Snipping Tool などで画像をコピー。
2. Codex CLI の PowerShell をフォーカス。
3. F8 を押すと、画像が `snips` に保存され、ファイルパスが PowerShell に自動入力される（見えない場合は矢印キー入力などで再描画）。

## セットアップ手順
1. リポジトリをクローンまたはファイルをダウンロード
2. `snip_hotkey.py` があるディレクトリに移動
3. Pythonライブラリをインストール:
   - `pip install Pillow keyboard`
4. 実行:
   - バックグラウンド起動: `pythonw snip_hotkey.py`
   - 通常起動（ログ表示）: `python snip_hotkey.py`

## 自動起動設定（Windows）
スタートアップフォルダにバッチファイルを配置:
```cmd
copy snip_hotkey_start.cmd "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\"
```

## 環境変数での設定変更
- `SNIP_HOTKEY_SAVE_DIR`: 画像保存ディレクトリ（デフォルト: `%USERPROFILE%\Documents\snips`）
- `SNIP_HOTKEY_LOG_PATH`: ログファイルパス（デフォルト: `snip_hotkey.log`）
