# Day 06 · Data Ingestion Engineering

> ## Bài làm — Trần Văn Tài (2A202603506)
>
> **Corpus:** OpenStax *Introduction to Python Programming* (CC BY-NC-SA 4.0), chương 4–6, 76/80 trang PDF có nội dung — [data/manifest.json](data/manifest.json).
> **Embedding:** OpenAI `text-embedding-3-small` (1536 chiều). **Vector store:** PostgreSQL 16 + pgvector 0.8.7, bảng `day6_chunks`, cosine chính xác (không ANN).
> **Chiến lược:** A fixed 500/50 · B theo đoạn/heading ≤800 · C = B + filter `chapter` — [artifacts/experiment_log.csv](artifacts/experiment_log.csv).
> **Benchmark:** 26 câu (20 dev / 6 test) — [benchmark/](benchmark/README.md). **Kết quả và audit:** [starter/results/](starter/results/). **Báo cáo:** [report/individual/2A202603506_TranVanTai.md](report/individual/2A202603506_TranVanTai.md).
>
> | Strategy | Dev Hit@1 | Dev Evidence Hit@3 | Test Hit@1 | Test Evidence Hit@3 | Coherence /2 | Grounding /2 (test) |
> |---|---|---|---|---|---|---|
> | A | 4/20 | 12/20 | 0/6 | 3/6 | 1,2 | 1,00 |
> | B | 14/20 | 20/20 | 2/6 | 4/6 | 1,8 | 1,67 |
> | **C (chọn trên dev)** | 15/20 | 20/20 | 3/6 | 5/6 | 1,8 | 1,83 |
>
> ### Chạy lại (cần Docker + Python 3.11–3.14 + OpenAI API key)
>
> ```bash
> cd starter
> python -m venv .venv                       # Windows: .venv\Scripts\activate ; macOS/Linux: source .venv/bin/activate
> python -m pip install -r requirements.txt
> cp .env.example .env                       # Windows PowerShell: Copy-Item .env.example .env ; rồi điền OPENAI_API_KEY
> docker compose -p day6_student_starter up -d --wait
> python scripts/check_setup.py
> python scripts/download_corpus.py          # tải PDF, kiểm tra SHA-256
> python scripts/build_manifest.py           # -> ../data/manifest.json, results/ingestion_log.txt
> python scripts/verify_benchmark.py         # kiểm chứng evidence trên trang gold
> python -m src.run ingest                   # chunk A/B, embed, upsert; chạy lần 2 để kiểm tra không trùng
> python -m src.run evaluate --split dev
> python -m src.run evaluate --split test    # chỉ sau khi chọn cấu hình trên dev
> python -m src.run audit                    # tạo bảng chấm thủ công (ghi đè file audit — sao lưu nhãn trước)
> ```
>
> ---

**Lab cá nhân** · **4 giờ** · **Dữ liệu tự chọn**

Biến tài liệu thành kho tri thức có thể truy xuất cho AI agent, rồi đo xem cách chuẩn bị dữ liệu nào hiệu quả nhất.

| 📄 Dữ liệu | 🧩 Chiến lược | 🎯 Benchmark |
|---|---|---|
| Tối thiểu **30 trang nội dung** | Tối thiểu **3 cấu hình** | Tối thiểu **20 câu hỏi** |

## Bắt đầu nhanh

Dùng [starter PostgreSQL + pgvector](starter/README.md) để dựng database và hoàn thiện các hàm TODO, hoặc tự chọn vector store tương đương. Starter chỉ là khung: **bạn tự hiện thực pipeline và benchmark**.

## 1. Xây pipeline

![Đọc tài liệu, chuẩn hóa, chia chunk, tạo vector, lưu và kiểm tra](assets/ingestion-pipeline.svg)

Chọn tài liệu được phép sử dụng; giữ **ID tài liệu, nguồn, trang/vị trí** và metadata phù hợp. Dùng embedding model thật qua API hoặc chạy local; lưu và truy xuất bằng pgvector, Qdrant, Chroma hoặc một store tương đương.

## 2. So sánh và đánh giá

![Ba chiến lược được đánh giá trên cùng corpus và benchmark dev/test](assets/benchmark-workflow.svg)

Dùng cùng dữ liệu, model và câu hỏi cho cả ba cấu hình. Tách **15 câu dev / 5 câu test** trước khi chạy; chọn cấu hình trên dev, rồi đánh giá test sau khi cố định. Mỗi câu hỏi cần có đoạn bằng chứng và trang nguồn; thiết kế bộ câu hỏi và đánh giá theo [BENCHMARK.md](BENCHMARK.md).

Đánh giá theo năm khía cạnh: **độ chính xác truy xuất**, **tính mạch lạc của chunk**, **tính hữu dụng của metadata**, **chất lượng grounding** và **tác động của chiến lược dữ liệu**. Giải thích lựa chọn bằng kết quả, ví dụ lỗi và các đánh đổi.

## 3. Chuẩn bị bài nộp

1. Chạy pipeline và lưu cấu hình, kết quả top-3, trace cùng nhãn đánh giá thủ công.
2. Điền [thông tin học viên](STUDENT.md), [nhật ký thí nghiệm](artifacts/experiment_log.csv) và bản sao [mẫu báo cáo cá nhân](report/individual/MSSV_HoTen.md).
3. Kiểm tra mã nguồn, cách chạy, manifest dữ liệu và checklist trong [SUBMISSION.md](SUBMISSION.md).

## Tài liệu hướng dẫn

| Bạn cần tìm | Tài liệu |
|---|---|
| Setup baseline PostgreSQL + pgvector | [starter/README.md](starter/README.md) |
| Các bước làm và cách tính chỉ số | [GUIDE.md](GUIDE.md) |
| Tiến độ trong 4 giờ | [CHECKPOINTS.md](CHECKPOINTS.md) |
| Năm tiêu chí benchmark và bộ câu hỏi | [BENCHMARK.md](BENCHMARK.md) |
| Tiêu chí chấm điểm | [RUBRIC.md](RUBRIC.md) |
| Quy tắc sử dụng dữ liệu, AI và API | [RULES.md](RULES.md) |
| Cách nộp bài | [SUBMISSION.md](SUBMISSION.md) |

[data/format-example.json](data/format-example.json) chỉ minh họa định dạng, không phải corpus đủ điều kiện. Phần xử lý và benchmark do bạn tự hiện thực; không bắt buộc xây chatbot.
