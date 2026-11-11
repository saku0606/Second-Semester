## パスパラメータ

### パスパラメータとは
URL の中で、**好きな値を指定できる場所**を `パスパラメータ` と呼びます。エンドポイントの中で `:変数名` と書くと、その部分がパスパラメータになります。

###### 書式
```js
app.get('/product/:id', (req, res) => {

});
```

| アクセスする URL | id の値 |
| ---- | ---- |
| http://localhost:3000/product/1 | 1 |
| http://localhost:3000/product/2 | 2 |
| http://localhost:3000/product/25 | 25 |

### パスパラメータの取得
パスパラメータは、リクエストオブジェクトの `req.params` から取得します。

| 項目 | 内容 |
| ---- | ---- |
| リクエストパラメータ | req.params |
| データの指定 | req.params.変数名 |
| 例 | req.params.id |

###### server.js
```js
app.get('/product/:id', (req, res) => {
    const id = req.params.id;
    console.log(id);
});
```

> `req.params` で取得した値は、**文字列**です。数値として使う場合は、`Number()` で変換します。

### 商品詳細ページ
`/product/:id` にアクセスしたら、`public/product.html` をレスポンスします。

| 項目 | 内容 |
| ---- | ---- |
| HTTP メソッド | GET |
| エンドポイント | /product/:id |
| ファイルパス | ./public/product.html |

###### server.js
```js
app.get('/product/:id', (req, res) => {
    const id = req.params.id;
    console.log("ルーティング: /product/" + id);
    res.sendFile(__dirname + '/public/product.html');
});
```

`http://localhost:3000/product/1` にアクセスして、商品詳細ページが表示されるか確認します。

> どの `id` でアクセスしても、同じ `product.html` が返ります。`id` に対応した商品の表示は、後ほど `API` と `CSR` で作成します。

## クエリパラメータ

### クエリパラメータとは
エンドポイントの後ろに付ける、`GET` パラメータです。`?` の後ろに `key=value` の形式で指定します。複数のパラメータは `&` で区切ります。

###### 書式
```txt
http://localhost:3000/search?keyword=shirt
http://localhost:3000/search?keyword=shirt&category=men
```

| 記号 | 内容 |
| ---- | ---- |
| ? | クエリパラメータの開始 |
| key=value | パラメータ名と値 |
| & | 複数パラメータの区切り |

### クエリパラメータの取得
クエリパラメータは、リクエストオブジェクトの `req.query` から取得します。

| 項目 | 内容 |
| ---- | ---- |
| クエリパラメータ | req.query |
| データの指定 | req.query.変数名 |
| 例 | req.query.keyword |

###### server.js
```js
app.get('/search', (req, res) => {
    const keyword = req.query.keyword;
    console.log(keyword);
});
```

`/search?keyword=shirt` にアクセスすると、`keyword` の値は `shirt` になります。

### パスパラメータとクエリパラメータの違い

| 項目 | パスパラメータ | クエリパラメータ |
| ---- | ---- | ---- |
| 例 | /product/1 | /search?keyword=shirt |
| 取得 | req.params | req.query |
| 主な用途 | 対象の指定（ID など） | 検索、絞り込み |

### キーワード検索（トップページ）
トップページの検索フォームから、キーワードを受け取ります。フォームは、`GET` リクエストで `/search` にキーワードを送信します。

###### public/home.html
```html
<form action="/search" method="get">
    <input id="keyword" type="text" name="keyword" placeholder="Search products...">
    <button type="submit">Search</button>
</form>
```

| 項目 | 内容 |
| ---- | ---- |
| HTTP メソッド | GET |
| エンドポイント | /search |
| ファイルパス | ./public/home.html |
| クエリパラメータ | keyword |

###### server.js
```js
app.get('/search', (req, res) => {
    console.log("ルーティング: /search");
    if (req.query.keyword) {
        const keyword = req.query.keyword;
        console.log("検索キーワード: " + keyword);
    }
    res.sendFile(__dirname + '/public/home.html');
});
```

検索フォームにキーワードを入力して送信すると、ターミナルにキーワードが表示されます。

###### 結果
```txt
ルーティング: /search
検索キーワード: shirt
```

> 検索結果の表示は、後ほど `API` と `CSR` で作成します。

## ミドルウェア

### ミドルウェアとは
`ミドルウェア` は、**リクエストとレスポンスの間で動く中間処理**です。どんなリクエストが来ても、まずミドルウェアを通してから、ルーティング処理が実行されます。アプリケーションの共通処理を登録するときに使います。

<img src="/storage/teaching_material/express_middleware_flow.svg" width="400">

### ミドルウェアの登録
ミドルウェアは、`use()` で登録します。

###### 書式
```js
app.use(ミドルウェアの処理);
```

### ミドルウェアの例

| ミドルウェア | 内容 |
| ---- | ---- |
| app.use((req, res, next) => { ... }) | カスタム処理（ログ、エラーハンドリングなど） |
| app.use(express.json()) | JSON データの受け取り |
| app.use(express.urlencoded({ extended: true })) | フォーム送信データの受け取り（application/x-www-form-urlencoded） |
| app.use(express.static('public')) | 静的コンテンツ（HTML、CSS、JS、画像など）の公開 |

###### server.js
```js
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
```

> `express.json()` を登録すると、`POST` で送信した `JSON` が `req.body` から取得できます。

### カスタム処理
すべてのルーティング処理の**直前**で実行される処理を作成します。サーバーのログやエラーハンドリングなどで利用します。

**処理が終わったら、`next()` で次の処理に進みます。** `next()` を呼ばないと、リクエストが止まったままになります。

###### server.js
```js
app.use((req, res, next) => {
    console.log(`ミドルウェア: ${req.method} ${req.url}`);
    next();
});
```

| 引数 | 内容 |
| ---- | ---- |
| req | リクエスト |
| res | レスポンス |
| next | 次の処理に進む関数 |

> ミドルウェアは、**ルーティングよりも前**に記述します。後ろに書くと、実行されません。

### ミドルウェアの確認
トップページ `/` に `GET` リクエストを送信します。ミドルウェアが実行されてから、ルーティング処理が実行されます。

###### 結果
```txt
ミドルウェア: GET /
ルーティング: /
```

## 静的コンテンツ

### 静的コンテンツとは
サーバー側で内容が変化せず、**そのまま返すファイル**です。画像、`HTML`、`CSS`、`JS` ファイルなどが該当します。

### 静的コンテンツのアクセス
`public` フォルダに、画像、`CSS`、`JS` などを配置します。ただし、このままでは**外部から直接アクセスできません**。

`home.html` に、次のように `JS` ファイルを読み込むタグがあります。

###### public/home.html
```html
<script src="/js/product/list.js"></script>
```

ブラウザが `/js/product/list.js` をリクエストしますが、対応するルーティングがないため、`404` エラー（`Not Found`）になります。

###### 結果（ターミナル）
```txt
ミドルウェア: GET /js/product/list.js
```

### public フォルダの公開
`express.static()` のミドルウェアで、`public` フォルダを公開します。`Express` が静的コンテンツを自動でレスポンスします。

###### server.js
```js
app.use(express.static(__dirname + '/public'));
```

| 項目 | 内容 |
| ---- | ---- |
| express.static() | 指定したフォルダの静的コンテンツを公開 |
| __dirname + '/public' | 公開するフォルダ |

### 公開したコンテンツの確認
`public` フォルダのパスが、URL のルート（`/`）になります。

| フォルダ内のファイル | アクセスする URL |
| ---- | ---- |
| public/images/Hoodie.png | /images/Hoodie.png |
| public/js/product/list.js | /js/product/list.js |
| public/css/default.css | /css/default.css |

> URL に `public` は含めません。

### 静的コンテンツの問題点
`public` フォルダを公開すると、**`HTML` ファイルにも直接アクセスできます**。たとえば、`/about.html` で About ページが表示されます。

ルーティングで制御した `/about` とは別の URL でアクセスできてしまうため、外部からアクセスできない場所で `HTML` を管理する必要があります。

> この問題は、テンプレートエンジンを学習するときに解決します。

## API ルーティングと CSR

### CSR とは
`CSR`（`Client Side Rendering`）は、サーバーからベースの `HTML` を取得し、**`JavaScript` で HTML を完成させる**方式です。画面の内容は、サーバーから `API` でデータを取得して描画します。

<img src="/storage/teaching_material/express_csr_flow.svg" width="600">

| 方式 | HTML を完成させる場所 |
| ---- | ---- |
| SSR | サーバー |
| CSR | ブラウザ（JavaScript） |

### 商品リストの取得（クライアント）
`/js/product/list.js` では、`Fetch API` で `GET` リクエストを送信し、`/api/product/list` から商品データを取得します。取得したデータを `CSR` で画面に描画します。

###### public/js/product/list.js
```js
// APIリクエスト
const res = await fetch("/api/product/list");
// サーバレスポンス
const data = await res.json();
// CSR処理
renderProducts(data.products);
```

`API` を作成していない状態では、ルーティングがないため、エラーになります。

### 商品リスト API（サーバ）
次のルーティングを作成します。

| 項目 | 内容 |
| ---- | ---- |
| HTTP メソッド | GET |
| エンドポイント | /api/product/list |
| レスポンス | JSON |

###### server.js
```js
app.get('/api/product/list', (req, res) => {
    // データ取得とレスポンス
});
```

### 商品データ
商品データは、`data/products.json` に配列形式の `JSON` で保存されています。

###### data/products.json
```json
[
    {
        "id": 1,
        "category": "men",
        "name": "Oxford Shirt",
        "note": "Classic fit for men",
        "price": 4500,
        "image": "images/Oxford-Shirt.png",
        "tag": null
    },
    ...
]
```

| 項目 | 内容 |
| ---- | ---- |
| id | 商品 ID |
| category | カテゴリ（men、women） |
| name | 商品名 |
| note | 商品の説明 |
| price | 価格 |
| image | 画像のパス |
| tag | タグ（SALE など） |

### カスタムモジュール
商品データを取得する処理は、`models/Product.js` にまとめます。`server.js` に処理を書き込まず、**役割ごとにファイルを分けるとプログラムが見やすくなります**。

| 関数名 | 役割 | 引数 | 戻り値 |
| ---- | ---- | ---- | ---- |
| fetchProducts() | 商品データの全件読み込み | なし | 商品の配列 |
| findProductById(id) | ID による商品の検索（1件） | id | 商品オブジェクト |
| searchProducts(keyword) | キーワードによる商品の検索 | keyword | 一致した商品の配列 |

### データの取得
`fetchProducts()` は、`fs.readFileSync()` で `JSON` ファイルを読み込み、`JSON.parse()` で `JavaScript` のオブジェクトに変換して返します。

###### models/Product.js
```js
import fs from 'fs';
import path from 'path';

const __dirname = path.resolve();
const filePath = path.join(__dirname, 'data', 'products.json');

export function fetchProducts() {
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data);
}
```

| 処理 | 内容 |
| ---- | ---- |
| export | 他のファイルから使えるように公開 |
| fs.readFileSync() | ファイルの同期読み込み |
| JSON.parse() | JSON 文字列からオブジェクトへの変換 |

### モジュールのインポート
`server.js` で、作成したモジュールを `import` します。自作のファイルは、パスを `./` から指定し、**拡張子 `.js` まで**記述します。

###### server.js
```js
import { fetchProducts } from './models/Product.js';
```

### 商品リスト API の実装
`fetchProducts()` で商品データを取得し、`res.json()` で `JSON` に変換してレスポンスします。

###### server.js
```js
app.get('/api/product/list', (req, res) => {
    const products = fetchProducts();
    const data = { products };
    res.json(data);
});
```

`http://localhost:3000/api/product/list` にアクセスすると、`JSON` が表示されます。

###### 結果
```json
{"products":[{"id":1,"category":"men","name":"Oxford Shirt", ... }]}
```

トップページを開くと、`list.js` が `API` からデータを取得し、`CSR` で商品リストを表示します。

### 商品 ID 検索 API
パスパラメータで商品 ID を受け取り、該当する商品を返す `API` を作成します。

| 項目 | 内容 |
| ---- | ---- |
| エンドポイント | /api/product/show/:id |
| パスパラメータ | req.params.id |
| データ検索 | findProductById(id) |
| レスポンス | JSON |

###### server.js
```js
import { fetchProducts, findProductById } from './models/Product.js';

app.get('/api/product/show/:id', (req, res) => {
    const id = Number(req.params.id);
    const product = findProductById(id);
    res.json(product);
});
```

商品詳細ページ `/product/1` を開くと、`API` からデータを取得し、`CSR` で商品詳細を表示します。

#### 商品が見つからない場合
存在しない `id` が指定されたときは、**`404` のエラーを返す**ようにします。`res.status()` で、ステータスコードを設定します。

###### server.js
```js
app.get('/api/product/show/:id', (req, res) => {
    const id = Number(req.params.id);
    const product = findProductById(id);
    if (!product) {
        return res.status(404).json({ error: "Product not found" });
    }
    res.json(product);
});
```

###### 結果（/api/product/show/99）
```json
{"error":"Product not found"}
```

### キーワード検索 API
クエリパラメータでキーワードを受け取り、一致した商品を返す `API` を作成します。

| 項目 | 内容 |
| ---- | ---- |
| エンドポイント | /api/search |
| クエリパラメータ | req.query.keyword |
| データ検索 | searchProducts(keyword) |
| レスポンス | JSON |

###### server.js
```js
import { fetchProducts, findProductById, searchProducts } from './models/Product.js';

app.get('/api/search', (req, res) => {
    const keyword = req.query.keyword || '';
    const products = searchProducts(keyword);
    res.json({ products });
});
```

> `req.query.keyword || ''` は、キーワードが指定されていないときに、空文字を初期値にする書き方です。

トップページの検索フォームにキーワードを入力すると、`/search?keyword=shirt` に移動します。`list.js` が `URL` のキーワードを読み取り、`/api/search` から検索結果を取得して `CSR` で表示します。

### API 一覧
この教材で作成した `API` は、次のとおりです。

| エンドポイント | HTTP メソッド | 内容 |
| ---- | ---- | ---- |
| /api/product/list | GET | 商品リストの取得 |
| /api/product/show/:id | GET | 商品 1 件の取得 |
| /api/search | GET | キーワードによる商品検索 |

## 課題

### 提出手順
作成した `05_express_1` プロジェクトを、次の手順で提出します。

| 手順 | 内容 |
| ---- | ---- |
| 1 | 「05_express_1」フォルダを複製 |
| 2 | 複製したフォルダ内の「node_modules」フォルダを削除 |
| 3 | 複製した「05_express_1」フォルダを ZIP に圧縮 |
| 4 | ファイル名を「05_express_出席番号_名前.zip」に変更 |

> `node_modules` は容量が大きく、`npm install` で再現できるため、削除してから提出します。

## まとめ

| 項目 | 内容 |
| ---- | ---- |
| パスパラメータ | /product/:id の形式。req.params で取得 |
| クエリパラメータ | /search?keyword=shirt の形式。req.query で取得 |
| ミドルウェア | リクエストとレスポンスの間の中間処理 |
| app.use() | ミドルウェアの登録 |
| next() | 次の処理への移動 |
| express.json() | JSON データの受け取り |
| express.urlencoded() | フォームデータの受け取り |
| express.static() | 静的コンテンツの公開 |
| CSR | ブラウザで JavaScript が HTML を完成させる方式 |
| res.json() | JSON のレスポンス |
| res.status() | ステータスコードの設定 |
| カスタムモジュール | 役割ごとに分けたファイル。import / export で利用 |
