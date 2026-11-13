# Benchmark — Introduction to Python Programming, chương 4–6

File câu hỏi: [questions.jsonl](questions.jsonl). Kiểm chứng evidence: `python scripts/verify_benchmark.py` (chạy từ `starter/`).

> **Trạng thái:** câu hỏi do AI (Claude) soạn nháp từ text đã chuẩn hóa, học viên đã duyệt và giữ nguyên (câu hỏi tiếng Anh). Ngày chốt: 2026-11-13, **trước mọi lần chạy truy xuất**.

## Cấu trúc

| | Dev | Test | Tổng |
|---|---:|---:|---:|
| Số câu | 20 | 6 | 26 |
| Câu có metadata filter | 2 (q04, q06) | 2 (q23, q26) | 4 |

Mỗi câu có: `id`, `split`, `type` (direct / paraphrase / condition / exception / metadata_filter), `question`, `expected_answer`, `gold_source_id`, `gold_page` (số trang PDF vật lý), `evidence_quote` (trích nguyên văn), `filter`, và `alternatives` khi có nhiều trang hợp lệ (q14, q23 — trang tóm tắt chương 143 lặp lại cùng ý). Câu hỏi viết bằng tiếng Anh cho cùng ngôn ngữ với corpus.

## Kiểm chứng evidence

`verify_benchmark.py` đọc lại PDF bằng cùng hàm `load_pdf` của pipeline, so khớp evidence với text trang gold sau khi gộp khoảng trắng, kiểm tra trang gold là trang nội dung được tính, giá trị filter trùng chương của trang gold, và số lượng dev/test/filter. Kết quả: 26/26 câu, 28/28 evidence (kể cả alternatives) có trên trang gold.

## Filter

- Trường lọc: `chapter` (4 = Decisions, 5 = Loops, 6 = Functions), lấy từ footer từng trang và mục lục.
- Filter là **input giả định được cung cấp trước khi truy xuất**: người học cho biết đang học chương nào. Giá trị không suy ra từ gold.
- Các câu filter được viết **mơ hồ nếu không biết chương**, để kiểm tra giá trị thật của filter:
  - q04 (ch4) và q23 (ch5): "else chạy khi nào" — if-else vs loop else.
  - q06 (ch4) và q26 (ch6): khoảng trắng quanh dấu `=` / toán tử theo PEP 8 — ch4 bảo bao quanh phép gán bằng một dấu cách, ch6 bảo không có dấu cách với keyword argument/default.
- Cấu hình C chỉ áp dụng filter cho 4 câu trên; 22 câu còn lại C chạy không filter (giống B).

## Cách chia dev/test và nguy cơ rò rỉ

Chia thủ công theo chương để test có đủ 3 chương (ch4: 1, ch5: 2, ch6: 3) và đủ loại câu (paraphrase, direct, exception, filter); câu test không dùng trang gold trùng với câu dev, trừ trang tóm tắt 143 (alternative của q14 dev và q23 test). Nguy cơ rò rỉ:
- q04/q23 và q06/q26 là các cặp cùng dạng; nhìn kết quả dev của q04/q06 có thể gợi ý hành vi của q23/q26.
- Cùng một corpus và cùng tác giả soạn câu cho cả dev và test.
- Test chỉ 6 câu: mỗi câu = ~17 điểm phần trăm, không đủ để kết luận tổng quát.

## Tiêu chí chọn cấu hình (chốt trước khi xem test)

Chọn trên **dev**, theo thứ tự ưu tiên:
1. Evidence Hit@3 trên dev cao hơn.
2. Nếu bằng nhau: Hit@1 trên dev cao hơn.
3. Nếu vẫn bằng: số chunk ít hơn (ít token embed, ít chi phí hơn).

Sau khi chọn, cố định cấu hình rồi mới chạy/đọc test. Không sửa câu hỏi, gold hay tham số sau khi xem test; nếu phải sửa sẽ ghi rõ trong báo cáo.

## Mẫu chấm coherence (chốt trước khi xem điểm)

10 vị trí nguồn = **ký tự ở giữa** (`len(text) // 2`) của text đã chuẩn hóa trên các trang nội dung thứ 0, 8, 16, …, 72 trong danh sách 76 trang đã sắp xếp: PDF **95, 103, 111, 119, 128, 136, 144, 153, 161, 169**. Với mỗi chiến lược, chấm chunk chứa vị trí đó theo thang 0–2 trong GUIDE.
