# 流程圖設計 (Flowchart)

本文件根據 [PRD.md](./PRD.md) 與 [ARCHITECTURE.md](./ARCHITECTURE.md) 的設計，詳細說明「AI 學習助理平台」的使用者操作路徑（User Flow）、系統資料序列流動（System Flow），並條列出預計使用的 URL 路由對照表。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者從註冊進入系統到完成筆記與測驗的心智歷程（Happy Path）：

```mermaid
flowchart LR
    A([使用者造訪首頁]) --> B{判斷是否已登入？}
    B -->|否| C[登入 / 註冊頁面]
    C -->|驗證成功| D[學習儀表板 Dashboard]
    B -->|是| D
    
    D --> E[查看各科目分類]
    E -->|新增學習資料| F[上傳講義或貼上文字]
    F -->|系統載入與運算中| G[檢視 AI 筆記摘要頁面]
    
    G --> H{下一步操作？}
    H -->|我想複習一下| I[請求 AI 依據筆記產生測驗]
    H -->|回到首頁| D
    
    I --> J[進入測驗頁面作答]
    J -->|提交答案| K[查看成績與弱點分析建議]
    K --> D
```

## 2. 系統序列圖（Sequence Diagram）

以下序列圖展示了平台最核心的功能：**「使用者上傳講義，經過 AI 整理後存入資料庫並返回結果」** 的底層運作。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器端
    participant Flask Route as App / Controller
    participant AI Service as AI API (OpenAI/Gemini)
    participant Model
    participant DB as SQLite

    User->>Browser: 貼上講義並點擊「生成筆記」
    Browser->>Flask Route: POST /notes 包含表單資料
    
    Flask Route->>AI Service: 傳遞 prompt 與文字，請求整理摘要
    Note right of Flask Route: 等待外部 API 回應 (需考慮 Timeout)
    AI Service-->>Flask Route: 成功回傳 Markdown 筆記摘要
    
    Flask Route->>Model: 呼叫 NoteModel 建立新物件
    Model->>DB: 執行 INSERT INTO notes ...
    DB-->>Model: 儲存成功，返回 new_record_id
    Model-->>Flask Route: 實體資料建立完成
    
    Flask Route-->>Browser: HTTP 302 重導向至 /notes/{id}
    Browser->>Flask Route: GET /notes/{id} 取得單一筆記
    Flask Route-->>Browser: Jinja2 渲染完成的 HTML 筆記頁面
    Browser-->>User: 畫面呈現 AI 整理的筆記結果
```

## 3. 功能清單與路由對照表

根據上述的流程，以下對初步預期的端點 (Endpoints) 進行盤點：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明與預期行為 |
| :--- | :--- | :---: | :--- |
| 首頁/學習儀表板 | `/` | GET | 顯示登入使用者的學習總覽與近期筆記。 |
| 會員登入 | `/auth/login` | GET / POST | 顯示表單 / 驗證帳號密碼並建立 session。 |
| 會員註冊 | `/auth/register` | GET / POST | 顯示表單 / 新增使用者到資料庫。 |
| 會員登出 | `/auth/logout` | GET | 清除 session，導向首頁。 |
| 新增講義 | `/notes/new` | GET | 提供上傳檔案或貼上講義字串的表單。 |
| 生成AI筆記 | `/notes` | POST | 接收資料、呼叫 AI，成功後轉向該筆記明細。 |
| 檢視單一筆記明細 | `/notes/<int:note_id>` | GET | 使用 Jinja2 渲染展示特定筆記與摘要。 |
| 從筆記生成測驗 | `/quiz/generate/<int:note_id>`| POST | 將筆記字串發送 AI，生成對應之考題再寫入 DB。|
| 進行測驗頁面 | `/quiz/<int:quiz_id>` | GET | 顯示題目與選項供使用者作答。 |
| 提交測驗答案 | `/quiz/<int:quiz_id>/submit` | POST | 後端比對解答、計算分數並儲存此次作答紀錄。 |
| 觀看弱點分析結果 | `/quiz/<int:quiz_id>/result` | GET | 秀出錯題、正確解答以及學習建議。 |
