# conversation-tracker

Tools để track và sync lịch sử hội thoại Project Eagle lên Confluence.

---

## Scripts

### `analyze_conversation.py`
Đọc transcript của một hội thoại và trích xuất metadata (topic, category, tools used, messages, ...).

```powershell
# Phân tích một hội thoại
python analyze_conversation.py <conversation-uuid>

# Output JSON (dùng bởi push script)
python analyze_conversation.py <conversation-uuid> --json

# Phân tích tất cả và lưu cache
python analyze_conversation.py --all --output conv_analysis.json
```

---

### `confluence_oauth.py`
Lấy OAuth 2.0 access token để gọi Confluence API.

**Chỉ cần chạy 1 lần** (hoặc khi token hết hạn). Token được lưu vào `confluence_config.json`.

**Setup:**
1. Tạo OAuth app tại https://developer.atlassian.com/console/myapps/
   - Type: **OAuth 2.0 integration**
   - Callback URL: `http://localhost:8765/callback`
   - Permissions → Confluence: `read:confluence-content.all`, `write:confluence-content`, `read:confluence-space.summary`, `search:confluence`, `read:me`
2. Copy **Client ID** và **Client Secret** vào `confluence_config.json`:
   ```json
   {
     "client_id": "YOUR_CLIENT_ID",
     "client_secret": "YOUR_CLIENT_SECRET",
     "email": "nguyennguyenle997@gmail.com",
     "base": "https://nguyennguyenle997.atlassian.net",
     "space": "EAGLE"
   }
   ```
3. Chạy:
   ```powershell
   python confluence_oauth.py
   ```
   Browser sẽ mở → đăng nhập Atlassian → token được lưu tự động.

---

### `push_conversation_to_confluence.py`
Push metadata hội thoại lên Confluence.

**Yêu cầu:** `pip install requests`

**Auth mode** được detect tự động từ `confluence_config.json`:
- Nếu có `access_token` → dùng **OAuth 2.0 Bearer** (qua `api.atlassian.com`)
- Fallback → **Basic Auth** (API token cũ, có thể bị 403)

**Usage:**
```powershell
# Kiểm tra kết nối Confluence
python push_conversation_to_confluence.py --check-access

# Tìm và lưu space key
python push_conversation_to_confluence.py --find-space

# Push một hội thoại cụ thể
python push_conversation_to_confluence.py <conversation-uuid>

# Push tất cả hội thoại GTA-related
python push_conversation_to_confluence.py --all

# Override space key
python push_conversation_to_confluence.py --all --space EAGLE
```

**Page structure được tạo trong Confluence:**
```
🗂️ Conversation Log
├── 📊 Overview & Index
├── 🐛 Debug & Bug Fixes
│   ├── [2026-10-13] Aether Skin Setup (bc8612dc)
│   └── ...
├── 🗺️ Map & World Building
├── 🎵 Audio / Radio
├── 📱 UI / Phone / Menu
├── 🛠️ Tools & Utilities
├── 👥 Characters & AI
├── 📋 Project Management
└── 🤖 Agent Operations
```

---

## Configuration (`confluence_config.json`)

```json
{
  "email": "nguyennguyenle997@gmail.com",
  "base": "https://nguyennguyenle997.atlassian.net",
  "space": "EAGLE",
  "client_id": "",
  "client_secret": "",
  "access_token": "",
  "refresh_token": "",
  "cloud_id": "c9bd5d7e-4527-4793-ae12-d9c81f25ac24",
  "oauth_mode": true,
  "parent_page_id": ""
}
```

> ⚠️ **Không commit** `confluence_config.json` lên git — chứa credentials!

---

## Workflow tổng thể

```
1. Chạy confluence_oauth.py → lấy access_token
2. Chạy push_conversation_to_confluence.py --check-access → verify
3. Chạy push_conversation_to_confluence.py --all → push 31 main conversations
4. Sau mỗi hội thoại mới:
   python push_conversation_to_confluence.py <new-conv-id>
```

---

## Local Markdown Fallback

Nếu Confluence chưa accessible, logs được giữ ở:

`C:\Users\LENOVO\Desktop\GTA\docs\project-eagle\conversation-log\`

- `index.md` — Full table của tất cả GTA-related conversations
- `debug-bug-fixes.md` — Debug & Bug Fix conversations
- `map-world-building.md` — Map & World Building
- `audio-radio.md` — Audio / Radio
- `ui-phone-menu.md` — UI / Phone / Menu

---

## Status

| Item | Status |
|------|--------|
| `analyze_conversation.py` | ✅ Working, 61 convs analyzed |
| `confluence_oauth.py` | ✅ Ready — needs client_id/secret |
| `push_conversation_to_confluence.py` | ✅ Updated for OAuth + Basic Auth |
| Confluence auth | ⏳ Waiting for OAuth app setup |
| Pages pushed | ❌ 0 / 31 |
