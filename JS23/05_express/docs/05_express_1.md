## Express プロジェクトの準備

### 今回利用するパッケージ
この教材では、次の2つのパッケージを使います。

| パッケージ名 | 内容 |
| ---- | ---- |
| express | Web フレームワーク（Express サーバ） |
| dotenv | 環境変数の読み込み |

### プロジェクトの作成
配布されたプロジェクトは、すでに初期化済みで、`package.json` にパッケージ情報が書かれています。ただし、**パッケージそのものはインストールされていません**。

###### package.json
```json
"dependencies": {
  "dotenv": "^17.2.3",
  "express": "^5.1.0"
}
```

`package.json` の情報をもとに、`npm install`（または `npm i`）でパッケージをまとめてインストールします。

###### ターミナル
```shell
npm install
```

> `package.json` から環境を再現することを、スキャフォールディング（`Scaffolding`）と呼ぶこともあります。

#### 新規に作成する場合
プロジェクトを一から作成する場合は、`npm init` で初期化してから、パッケージをインストールします。

###### ターミナル
```shell
npm init -y
npm i express dotenv
```

### 設定ファイル .env
サーバーのホストやポートなどの設定は、プロジェクト直下の `.env` ファイルに記述します。

###### .env
```env
HOST=localhost
PORT=3000
SESSION_SECRET=mySecretKey
```

| 項目 | 内容 |
| ---- | ---- |
| HOST | ホスト名（localhost） |
| PORT | ポート番号（3000） |
| SESSION_SECRET | セッションで使う秘密の文字（任意の文字） |

> `SESSION_SECRET` は、セッションを学習するときに使います。今回は設定だけしておきます。

### モジュールシステムの設定
現代の `JavaScript` 開発では、`ESM`（`ES6`）で書くのが標準的です。`import` 文を使うには、`package.json` で設定が必要です。

設定がないと、`CommonJS` として扱われるため、`import` 文を使うと警告やエラーになります。

###### 結果
```txt
Warning: Module type of xxxx is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
```

`package.json` に `"type": "module"` を追加します。

###### package.json
```json
{
  ...
  "type": "module",
  ...
}
```

| 設定 | モジュールシステム | 読み込み |
| ---- | ---- | ---- |
| type の指定なし | CommonJS | require() |
| type が module | ESM | import |

## 自動再起動（watch）

### 現状の問題
プログラムを修正するたびに、毎回 `node` コマンドを実行して、サーバーを再起動する必要があります。これでは開発の効率が悪くなります。

###### ターミナル
```shell
node server.js
node server.js
node server.js
```

### ホットリロード
**ファイルを保存するたびに、プログラムを自動で再起動**する仕組みを、ホットリロード（`Auto Load`）と呼びます。`Node.js` では、`--watch` オプションで利用できます。追加のパッケージは必要ありません。

###### ターミナル
```shell
node --watch server.js
```

> `--watch` オプションは、`Node.js` 18.11 以降で利用できます。`node -v` でバージョンを確認してください。

### npm スクリプトの登録
毎回オプションを付けて入力するのは大変なので、`package.json` の `scripts` に登録します。

###### 書式
```json
"scripts": {
  "コマンド名": "実行するスクリプト"
},
```

コマンド名を `dev`、スクリプトを `node --watch server.js` として追加します。

###### package.json
```json
"scripts": {
  "dev": "node --watch server.js",
  "test": "echo \"Error: no test specified\" && exit 1"
},
```

### npm run で実行
`npm run コマンド名` で、登録したスクリプトを実行できます。裏側では、`scripts` に書いたスクリプトが実行されます。

###### ターミナル
```shell
npm run dev
```

| 実行するコマンド | 裏で実行されるスクリプト |
| ---- | ---- |
| npm run dev | node --watch server.js |

### サーバープログラム
動作確認用に、`server.js` で `.env` を読み込みます。`dotenv.config()` で、`.env` の内容が `process.env` から取得できます。

###### server.js
```js
import dotenv from 'dotenv';
dotenv.config();

const HOST = process.env.HOST || 'localhost';
const PORT = process.env.PORT || 3000;

console.log(`http://${HOST}:${PORT}/`);
```

> `|| 'localhost'` のように書くと、`.env` に設定がない場合の初期値になります。

### ホットリロードの確認
`npm run dev` を実行したまま、`server.js` を修正して保存します。**保存するたびに、自動で再起動**されます。

###### 結果
```txt
http://localhost:3000/
Restarting 'server.js'
http://localhost:3000/
```

> `.env` を修正しても、自動では再起動されません。`.env` を変更したときは、`Ctrl + C` で停止して、`npm run dev` を実行し直します。

## Express とは

### フレームワーク
`Express` は、`Web` アプリケーションを作るための**フレームワーク**です。フレームワークは、ラーメン店にたとえるとわかりやすくなります。

| 項目 | フレームワークなし | フレームワークあり |
| ---- | ---- | ---- |
| 材料 | 畑で小麦を収穫 | スープや麺が用意済み |
| 調理 | 麺をこねる、出汁をとる | 調理器具や厨房が用意済み |
| 開発者の作業 | すべて自分で用意 | どんな味にするかに集中 |

### Web フレームワークの機能
`Web` フレームワークには、`Web` 開発の基本機能が標準で搭載されています。

| 機能 | 内容 |
| ---- | ---- |
| ルーティング | URL に対応した処理の振り分け |
| リクエストとレスポンス | クライアントとのデータのやり取り |
| テンプレートエンジン | HTML の動的な生成 |
| 静的ファイル配信 | 画像、CSS、JS などの公開 |
| DB接続 | データベースとの連携 |
| セッション | ユーザー状態の管理 |
| セキュリティとエラー処理 | 攻撃対策、エラーの制御 |

### 代表的な JavaScript の Web フレームワーク

| フレームワーク | 特徴 |
| ---- | ---- |
| Express | 超軽量な古参のサーバー。自由度が高く、機能の独自実装が必要 |
| Next.js | React 系。SSR、SSG、CSR のすべてに対応 |
| Nuxt.js | Vue 系の Next.js |
| Remix | 後発。標準 Web API を重視し、ページ遷移が軽い |
| Hono | マイクロフレームワーク。高速なバックエンド API に最適 |

### Express の特徴

| 特徴 | 内容 |
| ---- | ---- |
| シンプルで軽量 | 豊富な拡張モジュール（エコシステム） |
| 自由度が高い | プログラムは若干面倒になる |
| 用途 | バックエンド API の構築に特化 |

### Express と http モジュールの比較
`http` モジュールで毎回書いていた面倒な処理を、`Express` では簡単に書けます。

| 項目 | http モジュール | Express |
| ---- | ---- | ---- |
| サーバー作成 | http.createServer() で処理を毎回記述 | app.listen() |
| ルーティング | if 文で手動プログラム（GET、POST、パラメータなど） | app.get()、app.post() など |
| HTML 表示 | fs で HTML ファイルを読み込み | res.sendFile() |
| JSON | HTTP ヘッダーの設定が必要 | res.json() |

## Express サーバの作成

### Express アプリの作成
`express` モジュールを `import` し、`express()` でサーバー（アプリケーション）を作成します。変数名は `app` にすることが多いです。

###### server.js
```js
import express from 'express';

const app = express();
```

### サーバの待機
`listen()` で、ポートとホストを指定してサーバーを待機させます。コールバック関数は、サーバーの起動後に実行されます。

###### server.js
```js
app.listen(PORT, HOST, () => {
    console.log(`Server running: http://${HOST}:${PORT}/`);
});
```

### ソース
`server.js` の全体は、次のとおりです。

###### server.js
```js
import dotenv from 'dotenv';
import express from 'express';

dotenv.config();

const HOST = process.env.HOST || 'localhost';
const PORT = process.env.PORT || 3000;

const app = express();

app.listen(PORT, HOST, () => {
    console.log(`Server running: http://${HOST}:${PORT}/`);
});
```

### サーバの起動確認
`npm run dev` でサーバーを起動し、ブラウザで `http://localhost:3000` にアクセスします。

###### 結果
```txt
Cannot GET /
```

ルーティングを設定していないため、エラーメッセージが表示されます。**エラーが表示されても、`Web` サーバーは起動しています。**

### サーバの停止
サーバーの停止は、起動中のターミナルで **`Ctrl + C`** を入力します。

<img src="/storage/teaching_material/node_express_stop.png" width="500">

## ルーティング

### ルーティングとは
`ルーティング（Routing）` は、**どの URL にアクセスされたら、どのプログラムを実行するか**を振り分ける仕組みです。

### エンドポイント
URL のうち、ホスト以降のパスを `エンドポイント` と呼びます。

| URL | エンドポイント |
| ---- | ---- |
| http://example.com/users | /users |
| http://example.com/login | /login |
| http://example.com/product/23 | /product/23 |

### ルーティングの基本
`Express` では、HTTP メソッド、エンドポイント、コールバック関数を指定して、ルーティングを設定します。

###### 書式
```js
app.get('/users', (req, res) => {

});
```

| 要素 | 内容 |
| ---- | ---- |
| app.get | HTTP メソッド（GET、POST など） |
| '/users' | エンドポイント（URL のパス） |
| コールバック関数 | アクセス時に実行する処理（リクエストとレスポンス） |

### ルーティングメソッド

| HTTP メソッド | Express の関数 | 主な用途 |
| ---- | ---- | ---- |
| GET | app.get() | サーバーからデータを取得 |
| POST | app.post() | サーバーに新しいデータを送信、登録 |
| PUT | app.put() | 既存データの更新（すべて置き換え） |
| PATCH | app.patch() | 既存データの部分的な更新 |
| DELETE | app.delete() | サーバー上のデータの削除 |
| ALL | app.all() | すべての HTTP メソッドに共通で反応 |

### レスポンスの主なメソッド

| メソッド名 | 用途 |
| ---- | ---- |
| res.send() | 文字列、オブジェクトなどの送信 |
| res.sendFile() | ファイルの送信 |
| res.json() | JSON データの送信（API でよく使う） |
| res.redirect() | 別の URL へのリダイレクト |
| res.status() | HTTP ステータスコードの設定 |

### send()
`res.send()` は、文字列やオブジェクトをレスポンスします。

- `Content-Type` は、自動で判別される
- **レスポンスは一度しか送信できない**

###### 書式
```js
res.send(テキスト);
```

### get() でルーティング
`GET` リクエストの `/test` にアクセスしたときの処理を作成します。

###### server.js
```js
app.get('/test', (req, res) => {
    const message = 'Hello, Express!';
    res.send(message);
});
```

| 項目 | 内容 |
| ---- | ---- |
| HTTP メソッド | GET |
| エンドポイント | /test |
| レスポンス | res.send() |

ブラウザで `http://localhost:3000/test` にアクセスし、「Hello, Express!」が表示されれば成功です。

<img src="/storage/teaching_material/node_express_hello.png" width="400">

### all() でルーティング
`app.all()` は、**すべての HTTP メソッド**でマッチします。

###### server.js
```js
app.all('/info', (req, res) => {
    const message = 'すべてのHTTPメソッドでこのルートにマッチします';
    res.send(message);
});
```

| 項目 | 内容 |
| ---- | ---- |
| HTTP メソッド | すべて |
| エンドポイント | /info |
| レスポンス | res.send() |

### post() でルーティング
`POST` リクエストの `/save` にアクセスしたときの処理を作成します。

###### server.js
```js
app.post('/save', (req, res) => {
    const message = 'POST リクエストを受け取りました';
    res.send(message);
});
```

| 項目 | 内容 |
| ---- | ---- |
| HTTP メソッド | POST |
| エンドポイント | /save |
| レスポンス | res.send() |

> `POST` リクエストは、ブラウザの URL からはアクセスできません。ブラウザで `/save` を開くと、`GET` リクエストになるため、`Cannot GET /save` と表示されます。

### ログの確認
`req` オブジェクトを使うと、リクエストの情報をログ表示できます。

###### server.js
```js
app.get('/test', (req, res) => {
    console.log(req.method);
    console.log(req.url);
    console.log(req.query);
    res.send('Hello, Express!');
});
```

| プロパティ | 内容 |
| ---- | ---- |
| req.method | HTTP メソッド |
| req.url | リクエストされた URL |
| req.query | クエリパラメータ |

## POST リクエストの確認

### POST リクエストの特徴
`POST` リクエストは、**データをブラウザの裏側でサーバーに送信**します。URL にデータが表示されないため、次のようなデータの送信に向いています。

- 更新系のデータ
- 個人情報
- 大量のデータ
- バイナリデータ

クライアントからは、`HTML` の `form` や `JavaScript` の `Fetch API` などで送信します。

### POST のテスト方法
`POST` リクエストは、ブラウザの URL からは確認できません。そこで、次のツールを使います。

| ツール | 内容 |
| ---- | ---- |
| Postman | GUI で API をテストするアプリ |
| cURL | HTTP リクエストを送信するコマンド |

### Postman
`Postman` は、`API` テストの定番ツールです。`Windows` と `Mac` のネイティブアプリがあり、`Web API` を GUI 操作でテストできます。

<a href="https://www.postman.com/" target="_blank">Postman</a>

| 画面の項目 | 内容 |
| ---- | ---- |
| HTTP メソッド | GET、POST など |
| リクエスト URL | 送信先の URL |
| ヘッダー、データ | リクエストの付加情報 |
| HTTP ステータス | レスポンスの結果 |
| レスポンスデータ | サーバーからの返答 |

### cURL
`cURL`（カール）は、HTTP リクエストを送信するコマンドです。ターミナルやプログラムから実行でき、`API` のテストから `Web` スクレイピング、脆弱性検査まで幅広く使われます。

###### 書式
```shell
curl http://example.com
```

主なオプションは、次のとおりです。

| 用途 | オプション |
| ---- | ---- |
| HTTP メソッド | -X |
| リクエストヘッダ | -H |
| リクエストボディ | -d |
| ファイルアップロード（multipart/form-data） | -F |

### cURL で POST リクエスト
`/save` に `POST` リクエストを送信します。`Windows`（`PowerShell`）では、`curl.exe` と入力します。

###### macOS / Linux
```shell
curl -X POST http://localhost:3000/save
```

###### Windows（PowerShell）
```shell
curl.exe -X POST http://localhost:3000/save
```

###### 結果
```txt
POST リクエストを受け取りました
```

### データを付けて送信
`-H` でヘッダ、`-d` でデータを指定します。次は、`JSON` データを送信する例です。

###### macOS / Linux
```shell
curl -X POST http://localhost:3000/save \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","age":23}'
```

###### Windows（PowerShell）
```shell
curl.exe -X POST http://localhost:3000/save `
  -H "Content-Type: application/json" `
  -d "{\"name\":\"Alice\",\"age\":23}"
```

> 送信した `JSON` をサーバーで受け取る方法は、次の教材（ミドルウェア）で学習します。

## SSR（サーバサイドレンダリング）

### SSR とは
`SSR`（`Server Side Rendering`）は、**サーバー側で HTML を完成させてから、まとめてブラウザに渡す**方式です。レンダリングは、ブラウザへの表示のことです。

<img src="/storage/teaching_material/express_ssr_flow.svg" width="600">

### SSR のメリットとデメリット

| 区分 | 内容 |
| ---- | ---- |
| メリット | 受け取るだけで UI を表示できる |
| メリット | ブラウザの負荷が低い |
| メリット | SEO（検索エンジン）に強い |
| デメリット | レスポンスが届くまで何も表示されない |
| デメリット | アクセスが多いとサーバーに負荷がかかる |
| デメリット | ユーザー操作の自由度が低く、リアルタイム処理に弱い |

### sendFile()
`res.sendFile()` は、指定したファイルの中身をレスポンスします。主に `HTML` ファイルの送信に使います。

- `Content-Type` は、自動で推定される
- **レスポンスは一度しか送信できない**
- ファイルパスは、**絶対パス**で指定する

###### 書式
```js
res.sendFile(ファイルパス);
```

### 現在のディレクトリ
絶対パスを作るため、プロジェクトのフォルダを `__dirname` に設定します。`path.resolve()` は、`node` コマンドを実行したフォルダの絶対パスを返します。

###### server.js
```js
import path from 'path';

const __dirname = path.resolve();
```

> `ESM` では `__dirname` が用意されていないため、自分で定義します。プロジェクトのフォルダで `npm run dev` を実行してください。

### ページのルーティング
`public` フォルダの `HTML` ファイルを、`SSR` で返すルーティングを作成します。

| ページ | エンドポイント | HTTP メソッド | ファイルパス |
| ---- | ---- | ---- | ---- |
| トップ | / | GET | public/home.html |
| About | /about | GET | public/about.html |
| キーワード検索 | /search | GET | public/home.html |
| 商品詳細 | /product/:id | GET | public/product.html |

> 「キーワード検索」と「商品詳細」は、次の教材で作成します。

### トップページ
`/` にアクセスしたら、`public/home.html` をレスポンスします。

###### server.js
```js
app.get('/', (req, res) => {
    const filePath = __dirname + '/public/home.html';
    res.sendFile(filePath);
});
```

`http://localhost:3000/` にアクセスして、トップページが表示されるか確認します。

### About ページ
`/about` にアクセスしたら、`public/about.html` をレスポンスします。

###### server.js
```js
app.get('/about', (req, res) => {
    const filePath = __dirname + '/public/about.html';
    res.sendFile(filePath);
});
```

`http://localhost:3000/about` にアクセスして、About ページが表示されるか確認します。

## まとめ

| 項目 | 内容 |
| ---- | ---- |
| npm install | package.json をもとにしたパッケージのインストール |
| .env | ホストやポートなどの設定ファイル |
| type: module | ESM（import 文）を使うための設定 |
| node --watch | ファイル保存時の自動再起動 |
| npm run dev | scripts に登録したコマンドの実行 |
| Express | Web アプリケーションを作るフレームワーク |
| express() / listen() | アプリの作成とサーバーの待機 |
| ルーティング | URL に対応した処理の振り分け |
| app.get() / post() / all() | HTTP メソッドごとのルーティング |
| res.send() | 文字列のレスポンス |
| cURL / Postman | POST リクエストのテストツール |
| SSR | サーバーで HTML を完成させて返す方式 |
| res.sendFile() | HTML ファイルのレスポンス |
