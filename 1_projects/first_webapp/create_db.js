// create_db.js
const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.join(__dirname, 'data.db');
const db = new Database(dbPath);

db.exec(`
  CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount INTEGER NOT NULL
  );

  DELETE FROM sales;

  INSERT INTO sales (date, amount) VALUES
  ('2025-06-27', 150),
  ('2025-06-28', 200),
  ('2025-06-29', 170),
  ('2025-06-30', 220);
`);

console.log('샘플 데이터 생성 완료');
db.close();
