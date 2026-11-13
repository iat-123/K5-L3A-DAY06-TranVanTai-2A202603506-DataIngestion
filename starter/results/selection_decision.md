# Chọn cấu hình trên dev (ghi trước khi chạy test)

Thời điểm ghi: 2026-11-13T11:05:09Z — trước lệnh `python -m src.run evaluate --split test`.

Tiêu chí đã chốt trong benchmark/README.md: (1) dev Evidence Hit@3, (2) dev Hit@1, (3) ít chunk hơn.

| Strategy | Dev Hit@1 | Dev Evidence Hit@3 | Chunks |
|---|---|---|---|
| A | 4/20 | 12/20 | 218 |
| B | 14/20 | 20/20 | 220 |
| C | 15/20 | 20/20 | 220 (dùng chung index B) |

(1) B = C = 20/20 > A. (2) C 15/20 > B 14/20 → **chọn C**. Khác biệt B–C trên dev chỉ 1 câu (q04), mẫu rất nhỏ.

Không thay đổi tham số, chunker, câu hỏi hay gold sau quyết định này.
