// TODO: bcrypt インポート
const bcrypt = require('bcrypt');

/**
 * 平文パスワードとハッシュの比較
 */
// 既存のハッシュ値
const hash = '$2b$10$DZfvGBqDyS2TVal7PfxpreZMIyG7OWu4ocUodf3FhfYtJmasfujYq';
// TODO: 平文パスワード
const password = '9999';
// TODO: 平文とハッシュの比較: compareSync()
const isAuth = bcrypt.compareSync(password, hash)

// 結果表示
let result = { password, hash, isAuth }
console.log('平文とハッシュの比較結果:');
console.table(result);

/**
 * 新しいハッシュ作成
 */ 
// 新しいパスワード（平文）
const newPassword = '2222';
// TODO: ソルト生成（文字）: genSaltSync() 
const salt = bcrypt.genSaltSync(10)
// TODO: ハッシュ化: hashSync()
const newHash = bcrypt.hashSync(newPassword, salt)

// 結果表示
result = { newPassword, newHash }
console.log('新しいパスワードのハッシュ化結果:');
console.table(result);

const isAuth2 = bcrypt.compareSync(newPassword, newHash)

console.log("新しいパスワードとハッシュの比較結果:");
console.log(isAuth2);