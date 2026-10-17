# BTH3 - Product Management Service

Bài thực hành 3 môn SOA - Dịch vụ quản lý sản phẩm (FastAPI).

## Kiến trúc

- Product Service (BTH3): port 8001, DB products.db
- Auth Service (BTH2): port 8000, DB users.db
- Xác thực qua JWT dùng chung SECRET_KEY giữa 2 service

## Cài đặt và chạy

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8001 --reload
