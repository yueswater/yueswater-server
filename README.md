# 岳氏礦泉水的部落格後端

這是[岳氏礦泉水](https://www.yueswater.com/)的核心引擎，基於 [Python Django](https://www.djangoproject.com/) 與 [Django REST Framework](https://www.django-rest-framework.org/) 建構。部落格支援文章管理、Markdown 渲染、按讚、留言、分享、圖片上傳及 JWT 驗證。

## 技術組合

* **Django 5.x** 與 **Django REST Framework (DRF)** 作為後端基礎框架。
* **SimpleJWT** 處理使用者驗證與 Token 刷新機制。
* **Cloudinary** 提供雲端圖片儲存服務，用於文章圖片與封面圖。
* **Poetry** 進行相依性管理與虛擬環境建置。
* **Framer Motion** 在前端配合呈現流暢的渲染效果。
* **Unfold** 提供現代化的 Django Admin 管理介面。

## 專案結構

本專案採用模組化架構，將不同功能拆分至獨立的 App 中：

* `apps/posts`：處理文章、分類與標籤的核心邏輯，支援 Markdown 內容存儲。
* `apps/users`：管理使用者帳號、頭像上傳及電子郵件驗證。
* `apps/interactions`：負責處理文章按讚、留言、分享及書籤功能。
* `apps/newsletter`：發送訂閱電子郵件與歡迎信。
* `config`：存放全域設定，包括 REST Framework、日誌記錄、SMTP 郵件伺服器及 Unfold 介面配置。
* `utils`：包含自定義的異常處理、圖片處理邏輯以及髒話過濾器。
* `docs`：包含資料庫模型設計文件 (DBML)。

## 核心功能說明


### 圖片上傳服務與持久化規則

後端提供 `/api/upload/` 端點處理圖片上傳請求。為了配合前端渲染需求，後端在上傳完成後會將圖片封裝成帶有特定屬性的 HTML 標籤存入資料庫。這些屬性包括自動生成的唯一識別碼（如 `id="fig-xxxx"`），確保文章內容在不同平台間遷移時，圖片的交互參照與編號邏輯能保持資料一致性。

### 身份驗證與令牌生命週期管理

後端實作了基於 JWT 的雙權杖機制，透過 `/api/auth/refresh/` 端點處理 Access Token 的續期。當前端偵測到 401 錯誤時，後端負責驗證 Refresh Token 的有效性並核發新權杖，這保證了長文編輯過程中自動儲存操作的連續性。此外，後端在數據寫入層整合了**髒話過濾器 (Bad Words Handler)**，從源頭維護互動內容的合規性。

### 增量更新與自動儲存支援

為支援前端的自動快照功能，後端 API 針對文章端點開放了 PATCH 方法。此機制允許系統僅傳送變動的欄位進行局部更新，顯著降低了每 30 秒一次的高頻率請求對伺服器產生的負擔，確保編輯器狀態能穩定地同步至資料庫。

## 環境設定

請參考 `.env.example` 設定以下環境變數以確保專案正常運行：

* `SECRET_KEY`：Django 安全密鑰。
* `CLOUDINARY_URL`：Cloudinary 服務連接字串。
* `CORS_ALLOWED_ORIGINS`：允許存取的來源網域（例如 `http://localhost:3000`）。
* `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`：用於發送驗證信的 SMTP 帳號資訊。

## 快速啟動

使用 Poetry 安裝環境並啟動伺服器：

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver 8088
```