# snip_hotkey ツール 詳細設計

## 1. 目的

- Windows 環境で Snipping Tool などでキャプチャした画像を、最小の操作で Codex CLI（PowerShell 上）に共有するためのユーティリティ。
- 「画像をファイルに保存 → パスをコピー → ターミナルに貼り付け」という手順を、
  - `Snip` → `Codex CLI フォーカス` → `F8` だけで完了させることを目的とする。

## 2. 配置・構成

- スクリプト本体
  - パス: `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\snip_hotkey.py`
  - 役割: グローバルホットキーを監視し、クリップボードの画像をファイル保存＋パス自動入力する。

- 画像保存ディレクトリ
  - パス: `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\snips`
  - 振る舞い: 存在しない場合は起動時に自動作成される。

- 自動起動スクリプト（スタートアップ）
  - CMD ファイル:  
    - パス: `C:\Users\B1443kouda\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\snip_hotkey_start.cmd`
    - 役割: Windows ログオン時に **最小化した PowerShell** で `py snip_hotkey.py` を起動する。
  - 通常はスタートアップで自動起動するため、手動起動は不要（再起動は `restart_snip_hotkey.cmd` を利用）。

## 3. 動作仕様

### 3.1 起動

1. Windows ログオン時に、スタートアップフォルダの `snip_hotkey_start.cmd` が自動実行される。
2. CMD の処理内容（概略）:
   - `cd /d "C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey"`
   - `start "snip_hotkey" /min pwsh -NoLogo -Command py snip_hotkey.py`
   - 最小化状態の PowerShell から `py` ランチャー経由でスクリプトを常駐起動する。
3. タスクバーに最小化された PowerShell が残るが、ロック復帰時もプロセスが維持されやすい。

### 3.2 snip_hotkey.py の仕様

- 依存ライブラリ
  - `Pillow` (`PIL.ImageGrab`)
  - `keyboard`

- 定数
  - `SAVE_DIR` = `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\snips`
    - 起動時に `os.makedirs(SAVE_DIR, exist_ok=True)` でディレクトリを保証する。

- ホットキー
  - 割り当て: `F8`
  - 登録: `keyboard.add_hotkey("f8", save_clipboard_image)`
  - 特徴:
    - システム全体に対するグローバルホットキー。
    - どのアプリがアクティブでも F8 押下で `save_clipboard_image()` が呼び出される。

- クリップボード処理
- 関数: `save_clipboard_image()`
- 処理フロー:
    1) 最大 5 回（0.1 秒間隔）で `ImageGrab.grabclipboard()` を呼び、画像が取得できるまで待つ。`None` のままなら中断し、`no image in clipboard after retries` をログ出力。
    2) 画像を取得できた場合:
       - タイムスタンプ文字列 `YYYYMMDD_HHMMSS` を `datetime.now().strftime("%Y%m%d_%H%M%S")` で生成。
       - 保存パス: `SAVE_DIR` + `snip_YYYYMMDD_HHMMSS.png`
       - `img.save(path, "PNG")` で PNG 形式として保存。
       - `keyboard.write(f'"{path}"')` で、スペースを含むパスも安全に PowerShell へタイプする。
       - `snip_hotkey.log`（`LOG_PATH`）に保存完了・エラー内容などを追記する。

- メインループ
  - 関数: `main()`
  - 処理:
    - 起動メッセージを `print`。
    - `keyboard.add_hotkey("f8", save_clipboard_image)` でホットキー登録。
    - `keyboard.wait()` で無期限に待機（終了条件なし）。

### 3.3 通常利用時のユーザー操作フロー

1. ユーザーが Snipping Tool などで画面の一部をキャプチャし、クリップボードにコピーする。
2. Codex CLI が動作している PowerShell ウィンドウをアクティブにする。
3. キーボードで `F8` を押下する。
4. バックグラウンドで `save_clipboard_image()` が実行される:
   - `snips` フォルダに PNG ファイルが保存される。
   - そのファイルパスが PowerShell 上に自動で入力される。
5. ユーザーはそのまま Enter を押してファイルパスを Codex CLI に送信する。

## 4. 保守・運用上の注意点

### 4.1 Python / ライブラリ依存

- Python 実行ファイル
  - 起動コマンドは `py snip_hotkey.py`（Windows の py ランチャー前提）。
  - Python を別バージョンに入れ替えた場合も、`py` が新バージョンを指していればスクリプト修正は不要。

- 必須ライブラリ
  - `Pillow` と `keyboard` がインストールされていることが前提。
  - 新しい PC へ移行する場合:
    - `py -m pip install pillow keyboard` を一度実行しておくこと。

### 4.2 グローバルホットキーの競合

- `keyboard` ライブラリはシステム全体のキーボードフックを使用する。
- 他のソフトウェアが F8 をグローバルショートカットとして利用している場合、競合する可能性がある。
- 問題が出た場合の対処例:
  - 別のキー（`Ctrl+Alt+F8` など）に変更し、`keyboard.add_hotkey()` の引数を更新する。

### 4.3 エラー時の挙動

- 現在の実装では、予期しない例外（ファイル書き込み失敗など）が発生した場合、プロセスが終了する可能性がある。
- ただし、通常は以下で検知できる:
  - 再度 F8 を押してもパスが入力されなくなる。
  - タスクマネージャーで「ウィンドウタイトル: snip_hotkey」の PowerShell（`pwsh.exe`）が消えている。
- 再起動方法:
  - `C:\Users\B1443kouda\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\snip_hotkey_start.vbs` をダブルクリックする。

## 5. 将来の改善候補

- 例外処理
  - `save_clipboard_image()` を `try/except` でラップし、ログファイルや簡易ダイアログでエラー内容を記録する。

- 設定の外だし
  - 保存ディレクトリやホットキーを環境変数や設定ファイル（例: `snip_hotkey_config.json`）から読み込むようにし、PC 移行時にコード編集なしで変更できるようにする。

- ステータス確認用 UI
  - 現在は完全非表示のため、ユーザーからは「動いているかどうか」が分かりにくい。
  - 必要であれば、タスクトレイアイコンや簡易ログビューアを追加することで状態を可視化できる。

- ログ整理
  - 長期間の運用で `snips` フォルダに画像が溜まり続けるため、一定期間より古いファイルを削除するメンテナンススクリプトを別途用意することも検討する。


## 6. 運用手順（手動起動・停止）

### 6.1 手動起動

- スタートアップ経由ではなく、必要に応じて手動で起動する場合は、次のいずれかを実行する。

1. PowerShell / コマンドプロンプトから:
   - コマンド:
     - `\"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\snip_hotkey_start.cmd\"`
   - 効果:
     - スタートアップ時と同じ方法で、最小化 PowerShell から `py snip_hotkey.py` を起動する。

2. `restart_snip_hotkey.cmd` をダブルクリック:
   - パス:
     - `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\restart_snip_hotkey.cmd`
   - 効果:
     - 既存の「ウィンドウタイトルが snip_hotkey の PowerShell」だけを終了し、再度最小化 PowerShell で常駐起動する。

### 6.2 手動停止

- 完全非表示で起動しているため、通常はウィンドウからは終了できない。停止したい場合は以下のいずれかを行う。

1. タスクマネージャーから:
   - `Ctrl+Shift+Esc` でタスクマネージャーを開く。
   - 「詳細」タブ（または「プロセス」タブ）で、ウィンドウタイトルが `snip_hotkey` の PowerShell（`pwsh.exe`）を終了する。

2. 次回以降の自動起動を止める:
   - スタートアップフォルダから CMD ファイルを削除する。
   - 対象ファイル:
     - `C:\Users\B1443kouda\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\snip_hotkey_start.cmd`


## 7. ファイル配置と関連フォルダ

- メインスクリプト
  - `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\snip_hotkey.py`
- ログファイル
  - `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\snip_hotkey.log`
- 画像保存先
  - `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\snips`
- 関連ドキュメント
  - 本設計書: `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey\snip_hotkey_spec.md`

### 他ツールとの整理ルール

- Codex 用の補助スクリプトは `Obsidian Vault\Codex\tools` 配下に置き、用途ごとにサブフォルダに分割する。
  - 例: 進捗管理シート関連は `tools\progress_sheet` フォルダに集約。
- Snip ホットキー以外の一時的な検証スクリプトは、将来的に不要になったらこの progress_sheet フォルダ側で削除・整理する。
## 8. 常駐方式の方針変更（pythonw → 最小化 PowerShell）

- 以前は `pythonw.exe` を VBS から完全非表示で起動していたが、`Win+L`（ロック）や復帰後にプロセスが終了し、F8 が効かなくなる事象があった。
- 安定動作を優先し、**最小化した PowerShell ウィンドウで `py snip_hotkey.py` を実行する方式に変更**した。
  - タスクバーに小さな PowerShell ウィンドウが残るが、一般的にロックや休止状態からの復帰でもプロセスが維持されやすい。

### 8.1 現在の自動起動設定

- スタートアップフォルダの CMD
  - パス:
    - `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\snip_hotkey_start.cmd`
  - 内容（概略）:
    - `cd /d "C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey"`
    - `start "snip_hotkey" /min pwsh -NoLogo -Command py snip_hotkey.py`
- これにより、Windows ログオン時に最小化された PowerShell から `snip_hotkey.py` が常駐起動する。

### 8.2 手動再起動

- F8 が効かなくなった場合の復旧方法:
  1. `C:\Users\B1443kouda\Documents\Obsidian Vault\Codex\tools\snip_hotkey` にある
     `restart_snip_hotkey.cmd` をダブルクリックする。
  2. これにより、既存の `pythonw.exe`/PowerShell を停止し、新たに `py snip_hotkey.py` を最小化ウィンドウで起動する。

- ログ確認:
  - `snip_hotkey.log` の末尾（`Get-Content snip_hotkey.log -Tail 20`）を確認することで、
    F8 検知や画像保存・パス入力の成否を確認できる。

## 9. Notes (2025-11-21)

- restart_snip_hotkey.cmd now terminates only pwsh.exe processes whose window title is "snip_hotkey", so other PowerShell sessions (e.g. Codex CLI) are not killed.
- snip_hotkey.py now logs additional details:
  - "grabclipboard failed: ..." when ImageGrab.grabclipboard() raises an exception.
  - "add_hotkey failed: ..." when keyboard.add_hotkey("f8", save_clipboard_image) fails.
  - "hotkey registered" when the F8 hotkey registration succeeds.
- On this environment, the script should be started via "py snip_hotkey.py" instead of "python snip_hotkey.py".

## 10. Known issue: F8 hotkey becomes inactive (2025-11-21)

### 10.1 現象の概要
- `snip_hotkey.py` は常駐中 (`keyboard.add_hotkey("f8", save_clipboard_image)` + `keyboard.wait()`) で、`snip_hotkey.log` にも `snip_hotkey started (F8)` / `hotkey registered` が出ている。
- 起動直後は F8 で正常動作するが、しばらく他アプリを操作した後（例: ブラウザで GitHub Issue に入力 → 再び Codex CLI に戻る）に F8 を押しても、
  - 画像保存もパス入力も行われない。
  - `snip_hotkey.log` に `F8 pressed` のログが一切追加されない。
  - その時点でも `py.exe` / `python.exe` プロセスは生きている。
- つまり「プロセスは生きているが、`keyboard` ライブラリの F8 グローバルフックだけが途中で効かなくなる」状態になっている。

### 10.2 試したことと結果
- `restart_snip_hotkey.cmd` の改修
  - 以前: すべての `pwsh.exe` / `pythonw.exe` を強制終了していたため、Codex CLI の PowerShell まで巻き込んで落ちてしまっていた。
  - 現在: ウィンドウタイトルが `snip_hotkey` の `pwsh.exe` のみを kill し、その後最小化 `pwsh` から `py snip_hotkey.py` を起動する実装に修正済み。
- `snip_hotkey.py` のログ強化
  - F8 押下 (`F8 pressed`)、クリップボード取得エラー (`grabclipboard failed: ...`)、画像保存エラー (`save failed: ...`)、パス入力エラー (`keyboard.write failed: ...`) を `snip_hotkey.log` に出力するようにした。
  - 実際の停止時にはこれらのエラーは出ず、単に F8 が一切ログに現れない。
- PowerShell 側で F8 を受ける試み
  - `snip_hotkey.ps1` で Windows API (user32.dll) の RegisterHotKey / GetMessage を直接呼び出し、F8 を PowerShell 側で受け取ってから `py snip_hotkey.py` を一回実行する案を試験。
  - この試行中に RegisterHotKey(F8) failed ログが出るケースや、Add-Type のコンパイルエラーが発生し、現状では安定動作に至っていないため、一旦ロールバックした。

### 10.3 現時点の結論
- スクリプト側（`snip_hotkey.py`）に明確な例外や終了ログはなく、プロセスも残っていることから、
  - 根本原因は OS / 他プロセスとの低レベルキーフック競合、もしくは `keyboard` ライブラリ固有の挙動である可能性が高い。
  - 現状の情報だけでは「どのアプリ／イベントがトリガーか」を特定しきれない。
- そのため、`keyboard` ベースの F8 グローバルホットキーは、この環境では長時間の完全な安定運用は難しい。

### 10.4 当面の運用と将来の移行案
- 当面の運用
  - F8 が効かなくなった場合は `restart_snip_hotkey.cmd` を実行し、最小化 `pwsh` + `py snip_hotkey.py` を再起動する。
  - 再起動後も同様の症状が出た場合は、`snip_hotkey.log` と `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like ''*snip_hotkey.py*'' }` の結果を確認し、
    - プロセス存否
    - `F8 pressed` ログ有無
    を併せて記録する。
- 将来の移行案（推奨）
  - F8 グローバルホットキーの実装を `keyboard` から切り離し、次のような構成に移行する:
    - Windows ショートカット (`.lnk`) のホットキー、または AutoHotkey / 代替 PowerShell スクリプトで F8 を受ける。
    - F8 押下時に `py snip_hotkey.py` を「ワンショット」で起動し、
      - クリップボード画像の保存
      - ファイルパスの自動入力
      を Python にだけ任せる。
  - こうすることで、グローバルフックの責務を OS 側に任せ、`keyboard` ライブラリの不安定さの影響を受けにくくする。

## 11. Codex CLI の入力行再描画に関する注意 (2025-11-25)

- 現象:
  - F8 押下直後に、Codex CLI 側の入力行にファイルパスが「すぐには表示されず」、ユーザーが Enter や矢印キーなどを押したタイミングでまとめて表示される場合がある。
  - `snip_hotkey.log` 上は毎回 `typed path into active window` が出ており、`keyboard.write(path)` 自体は正常に動作している。
- 原因について:
  - Codex CLI の PowerShell 上の UI が、外部から送られたキーストロークだけでは入力行を即時再描画していない挙動と考えられる。
  - `keyboard.write()` 側からは通常のキー入力と同じイベントを送っており、Python スクリプト側だけで根本対応するのは難しい。
- 検討した案と結論:
  - `keyboard.send("enter")` や `keyboard.send("end")` など、追加のキー送信で再描画を強制する案を試したが、
    - Enter 送信案: パス入力直後に自動送信されてしまい、既存の対話フローと相性が悪い。
    - End 送信案: 実環境で Codex CLI のターミナルがクラッシュするケースがあり、安定運用に支障が出た。
  - そのため、現在は安全性を優先し、`keyboard.write(path)` のみを行うシンプルな実装に戻している。
- 運用上の推奨:
  - F8 押下後、もし入力行にパスが見えない場合でも、内部的には既にパスが入力されている前提とする。
  - 必要であれば、矢印キーやスペースなどを一度押して入力行を再描画させたうえで、Enter を押して送信する運用とする。
  - `snip_hotkey.log` に `typed path into active window` が出ていれば、スクリプトとしては正常動作していると判断できる。
