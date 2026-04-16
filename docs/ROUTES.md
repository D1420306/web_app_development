# 路由與頁面設計文件 (ROUTES)

本文件定義記帳簿系統所有的 API 路由、所屬的方法、與對應的 Jinja2 樣板，方便團隊在後續開發時對照。

## 1. 路由總覽表格

### 認證路由 (auth)
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 接收表單並建立 User，重導向到登入 |
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證密碼並建立 Session，重導向到儀表板 |
| 使用者登出 | GET/POST | `/auth/logout` | — | 刪除 Session 並重導向到登入頁 |

### 收支路由 (expense)
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 儀表板(首頁) | GET | `/` | `expense/dashboard.html` | 若未登入則重導向。顯示總覽 |
| 收支列表 | GET | `/expenses` | `expense/index.html` | 顯示所有收支列表 (可加上參數進行篩選) |
| 新增收支頁面 | GET | `/expenses/add` | `expense/add.html` | 顯示新增表單，需傳入分類清單 |
| 處理新增 | POST | `/expenses/add` | — | 處理表單後重導至 `/expenses` |
| 編輯收支頁面 | GET | `/expenses/<id>/edit`| `expense/edit.html`| 顯示編輯表單，帶入原紀錄內容 |
| 處理更新 | POST | `/expenses/<id>/edit`| — | 寫入 DB 並重導至 `/expenses` |
| 處理刪除 | POST | `/expenses/<id>/delete`| — | 驗證擁有者後刪除，重導至 `/expenses` |
| 統計報表 | GET | `/reports` | `expense/reports.html` | 顯示每月收支圖表或清單 |

### 分類維護 (category)
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 分類列表 | GET | `/categories` | `category/index.html` | 顯示已定義的分類列表與新增表單 |
| 新增分類 | POST | `/categories/add` | — | 新增專屬分類後重導回 `/categories` |
| 刪除分類 | POST | `/categories/<id>/delete`| — | 刪除指定專屬分類後重導回 `/categories` |

### 管理員 (admin)
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 查看會員清單 | GET | `/admin/users` | `admin/users.html` | 列出系統所有註冊者 (權限檢查) |

---

## 2. 每個路由的詳細邏輯說明

後續實作時，可直接參考 `app/routes/` 裡每個 Python 檔案中的 Docstring 說明，內含輸入與輸出的邏輯、DB Model 呼叫函式。

---

## 3. Jinja2 模板清單

所有的模板檔案將建置在 `app/templates` 底下，全部繼承自 `base.html`，以達到全域 Layout 共享的效果。

* `base.html`：包含 <head>、共用 Navbar、Flash Message 區塊與頁尾。
* `auth/`
  * `register.html`：繼承 base，提供 username, email, password 的表單。
  * `login.html`：繼承 base，提供 email, password 的表單。
* `expense/`
  * `dashboard.html`：繼承 base，顯示當前月份的收支摘要。
  * `index.html`：繼承 base，顯示列表與搜尋列。
  * `add.html`：繼承 base，收支填寫表單。
  * `edit.html`：繼承 base，帶有預設值的收支編輯表單。
  * `reports.html`：繼承 base，顯示圖表。
* `category/`
  * `index.html`：繼承 base，清單管理與單行新增表單。
* `admin/`
  * `users.html`：繼承 base，僅限 Role=admin 顯示的清單。
