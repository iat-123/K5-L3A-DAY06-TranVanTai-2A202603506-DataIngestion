# Báo cáo cá nhân — Day 6

**Học viên:** Trần Văn Tài · **MSSV:** 2A202603506 · **Ngày chạy:** 2026-11-13 (UTC)

## Dữ liệu và pipeline
- **Chủ đề, nguồn/quyền, số trang và quy tắc tính trang:** OpenStax *Introduction to Python Programming* (Das, Lawson, Mayfield, Norouzi; OpenStax, Rice University), PDF tải ngày 2026-11-13, SHA-256 `e1298e4f…383d`. Giấy phép **CC BY-NC-SA 4.0**, đọc trực tiếp ở trang 4 của PDF; dùng phi thương mại cho lab, có ghi nguồn. PDF không commit, `scripts/download_corpus.py` tải lại và kiểm tra checksum. Chọn chương 4–6 (Decisions, Loops, Functions), trang PDF 95–174 = 80 trang vật lý. Quy tắc: trang được tính khi text sau chuẩn hóa (bỏ footer) có ≥ 300 ký tự. Kết quả **76 trang nội dung, 83.764 ký tự**; loại 4 trang (124, 174 trống; 146 = 112 ký tự, 173 = 257 ký tự). Chi tiết từng trang: [data/manifest.json](../../data/manifest.json).
- **Chuẩn hóa, lỗi và giới hạn:** `pypdf` 6.21.4 trích từng trang; Unicode NFC; khoảng trắng lạ → dấu cách; gộp khoảng trắng nhưng giữ xuống dòng (cần cho heading và code). Footer lặp (`4.1 • Boolean values 87`, `Access for free at openstax.org`) được tách khỏi text và parse thành metadata `book_page`, chapter. Footer khớp mục lục ở 80/80 trang. Log: [ingestion_log.txt](../../starter/results/ingestion_log.txt). Giới hạn: trích PDF làm mất thụt lề của code Python (mọi dòng code thẳng hàng); công thức toán ở trang 164, 170 bị mất (ví dụ "acceleration in ." thiếu đơn vị); không có trang scan nên không dùng OCR; trang mở chương (95, 125, 147) không có footer chuẩn nên `book_page` rỗng.
- **Embedding, vector store, metric, lệnh chạy và chi phí:** OpenAI `text-embedding-3-small`, SDK `openai==2.54.0`, **1536 chiều** (đo bằng một lần gọi thử, không giả định). Query và document embed cùng cách, không có tiền tố. Vector store **PostgreSQL 16.16 + pgvector 0.8.7** (Docker `pgvector/pgvector:0.8.7-pg16`), bảng `day6_chunks`, **cosine chính xác** (`<=>`, không ANN index), filter bằng SQL `WHERE`. Lệnh chạy: xem mục "Bài làm" trong [README.md](../../README.md). Chi phí: embed A 24.865 token, B 22.819 token, câu hỏi 375 token, **tổng ≈ 0,001 USD**. Mức giá 0,02 USD/1M token theo bảng giá OpenAI mà tác giả dùng; cần đối chiếu lại nếu giá thay đổi.
- **Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn:** mỗi chunk có `document_id`, `source` (đường dẫn PDF; URL gốc nằm trong manifest), `page` (trang PDF vật lý), `start`/`end` (offset ký tự trong trang), `book_page`, `chapter_title`. Trường lọc: **`chapter` (int: 4/5/6)**, lấy từ khoảng trang trong mục lục và kiểm chéo với footer từng trang, nên không có giá trị nào là đoán. Lý do chọn: ba chương dùng cùng từ khóa với nghĩa khác nhau (`else` trong if-else và trong loop else; khoảng trắng quanh `=` trong phép gán và trong keyword argument). Người học thường biết mình đang học chương nào, nên chương là ngữ cảnh hợp lý để cung cấp trước khi truy xuất.

## Cấu hình và benchmark
- **A / B / C:**
  - **A:** `fixed_size`, cửa sổ 500 ký tự, overlap 50, cắt trong phạm vi một trang, không lọc. 218 chunk.
  - **B:** `by_paragraph`. Đoạn văn kết thúc ở dòng có dấu câu. Heading, callout (`CHECKPOINT`, `CONCEPTS IN PRACTICE`, `TRY IT`, `EXAMPLE x.y`) và tiêu đề mục ngắn mở chunk mới khi chunk hiện tại ≥ 80 ký tự. Gom đoạn đến tối đa 800 ký tự; đoạn quá dài cắt theo câu; mảnh dưới 100 ký tự gộp vào chunk bên cạnh. Không lọc. 220 chunk.
  - **C:** dùng **đúng chunk và vector của B**. Khác biệt duy nhất B–C là `WHERE chapter = <giá trị>`, chỉ áp dụng cho 4 câu có filter; 22 câu còn lại C chạy y hệt B.
  - Cả ba dùng cùng corpus, model, store, metric cosine và top-3.
- **≥20 câu:** 26 câu ([benchmark/questions.jsonl](../../benchmark/questions.jsonl)), chia trước **20 dev / 6 test**, có đủ loại direct, paraphrase, condition, exception, metadata_filter. **4 câu filter:** q04, q06 (dev, chương 4) và q23 (chương 5), q26 (chương 6) ở test. Câu filter được viết mơ hồ nếu không biết chương. Evidence được kiểm chứng bằng `scripts/verify_benchmark.py`: đọc lại PDF bằng chính hàm ingest, khớp nguyên văn evidence trên trang gold (bỏ qua khác biệt khoảng trắng), kiểm tra trang gold là trang được tính và filter khớp chương của trang gold. Kết quả 28/28 evidence, gồm 2 trang thay thế (trang tóm tắt 143 cho q14, q23). Câu hỏi do Claude soạn nháp, tác giả duyệt.
- **Tiêu chí chọn đã chốt trước khi xem test** ([benchmark/README.md](../../benchmark/README.md)): (1) Evidence Hit@3 trên dev, (2) Hit@1 trên dev, (3) ít chunk hơn. Quyết định ghi lúc 11:05:09Z, trước khi chạy test: [selection_decision.md](../../starter/results/selection_decision.md).

## Kết quả
| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian | Chi phí |
|---|---|---|---|---|---|---|
| A | dev | 4/20 | 12/20 | 218 | ingest 1,7 s (embed 1,4 s + ghi DB 0,3 s); 20 truy vấn 0,46 s | ≈ 0,0005 USD (24.865 token) |
| A | test | 0/6 | 3/6 | 218 | 6 truy vấn 0,21 s | (đã gồm ở trên) |
| B | dev | 14/20 | 20/20 | 220 | ingest 1,3 s (embed 1,0 s + ghi DB 0,32 s); 20 truy vấn 0,53 s | ≈ 0,0005 USD (22.819 token) |
| B | test | 2/6 | 4/6 | 220 | 6 truy vấn 0,17 s | (đã gồm ở trên) |
| C | dev | 15/20 | 20/20 | 220 (chung với B) | không ingest thêm; 20 truy vấn 0,58 s | 0 thêm |
| C | test | 3/6 | 5/6 | 220 (chung với B) | 6 truy vấn 0,20 s | 0 thêm |

Phân bố độ dài chunk (ký tự):

| Index | Số chunk | min | trung vị | trung bình | max | Tổng ký tự | Token embed |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 218 | 51 | 500 | 416,8 | 500 | 90.864 | 24.865 |
| B (= C) | 220 | 105 | 313,5 | 380,1 | 790 | 83.620 | 22.819 |

Nạp lại lần 2: 0 chunk embed lại, 0 dòng trùng (218 và 220 dòng giữ nguyên); chunk lỗi thời sẽ bị xóa theo `document_id` ([ingest_runs.jsonl](../../starter/results/ingest_runs.jsonl)). Embed câu hỏi: 286 token (dev), 89 token (test). Thời gian là một lần chạy trên máy cá nhân, gọi qua mạng, nên chỉ mang tính tham khảo.

| Strategy | Coherence trung bình /2 (n) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N hoặc N/A) | Grounding 0/1/2 (số câu) và trung bình /2 |
|---|---|---|---|---|
| A | 1,2 (n = 10) | 18/18 | dev 0/2 · test 0/2 | 2 / 2 / 2 · 1,00 |
| B | 1,8 (n = 10) | 18/18 | dev 0/2 · test 0/2 | 0 / 2 / 4 · 1,67 |
| C | 1,8 (n = 10, chung chunk với B) | 18/18 | dev 2/2 · test 2/2 | 0 / 1 / 5 · 1,83 |

Filter tuân thủ = số câu filter có cả top-3 thuộc đúng chương. A và B không lọc, cột này cho thấy kết quả "tự nhiên" có nằm trong chương được yêu cầu hay không.

**Đường dẫn trace, nhãn thủ công và cách chọn mẫu:** trace đầy đủ top-3 (text, score, metadata, cờ hit) ở [traces_dev.jsonl](../../starter/results/traces_dev.jsonl) và [traces_test.jsonl](../../starter/results/traces_test.jsonl); chỉ số ở `metrics_dev.json`, `metrics_test.json`. Coherence: [coherence_audit.md](../../starter/results/coherence_audit.md). 10 vị trí chốt trước là ký tự giữa trang trên các trang nội dung thứ 0, 8, …, 72 (PDF 95, 103, 111, 119, 128, 136, 144, 153, 161, 169). Tác giả tự chấm, có lý do từng nhãn. Metadata và grounding: [test_audit.md](../../starter/results/test_audit.md), 6 câu test × A/B/C × top-3. Nhãn do Claude đề xuất, tác giả duyệt và giữ nguyên. Quy tắc grounding ghi ở đầu file.

## Phân tích và kết luận
- **So sánh A–B (chỉ đổi chunking):** B hơn A rõ ở mọi chỉ số: Evidence Hit@3 dev 20/20 so với 12/20, Hit@1 dev 14/20 so với 4/20, coherence 1,8 so với 1,2. Kiểm tra từng câu A trượt trên trang gold cho thấy hai nguyên nhân:
  1. **Evidence bị cắt ngang thật:** chỉ 1/8 câu dev (q17, trang 156) và 1/3 câu test (q25, trang 170); không cửa sổ nào chứa đủ câu evidence.
  2. **Chunk đúng không lọt top-3:** 7/8 câu dev còn lại có một cửa sổ A chứa đủ evidence, nhưng cửa sổ đó lẫn nửa ý trước/sau nên xếp dưới các cửa sổ khác. Ví dụ **q07** (trang 111): cả 3 kết quả đều thuộc trang 111 (`A:00`, `A:02`, `A:03`) nhưng không phải `A:01`, chunk chứa câu "Two separate if statements do not guarantee…". `A:01` bắt đầu bằng mẩu từ "ngle condition" và kết thúc giữa câu "both if statements are" (coherence = 1).

  Như vậy cắt cố định làm hại chủ yếu vì chunk bị pha loãng ngữ nghĩa, ít khi vì làm mất evidence. A còn tốn hơn 9% token vì overlap (90.864 ký tự embed so với 83.620). Chi phí và thời gian của A và B gần như bằng nhau.
- **So sánh B–C (chỉ thêm filter):** khác biệt chỉ nằm ở 4 câu filter. Ví dụ **q04** (dev, ngữ cảnh chương 4, gold trang 102): B xếp hạng 1 chunk loop else ở trang 140 (chương 5, score 0,678) trên chunk if-else ở trang 102 (0,557). C lọc chapter=4 nên đưa trang 102 lên hạng 1. Ví dụ **q26** (test, chương 6, gold trang 171): B xếp hạng 1 đoạn PEP 8 chương 4 ở trang 110 ("Surround … assignment … with one space"), mâu thuẫn với đáp án đúng ở hạng 2. C đưa trang 171 lên hạng 1, grounding từ 1 lên 2. Filter tuân thủ: C 4/4, A và B 0/4.
- **Ví dụ sai của chiến lược được chọn (C):**
  - **q21** (test, gold trang 116, "How does Python show that one decision statement is placed inside another?"): cả ba cấu hình đều trượt. Top-3 của C là trang 95, 111, 100, đều là đoạn chung về câu lệnh điều kiện. Câu hỏi dùng cụm "placed inside another", sách dùng từ "Nesting"; câu có đáp án ở trang 116 nằm trong chunk ngắn `p116:B:02` (304 ký tự), mở đầu bằng dòng code thừa `print("Ready to start")` và chủ yếu nói về việc code ví dụ bị lặp ("The programmer realizes the code is redundant…"). Đây là lỗi lệch từ vựng, filter không giúp được vì câu không có filter.
  - **q23** (test, gold trang 141 hoặc 143): chỉ số tự động báo C có Evidence Hit@3 nhưng Hit@1 trượt. Hạng 1 là chunk trang 140 "A loop else statement runs after the loop's execution is completed without being interrupted by a break". Đúng ý nhưng câu vắt sang trang 141 nên thiếu chữ "statement", và trang 140 không có trong danh sách gold. Người chấm xác nhận đây là bằng chứng tương đương nhưng **không sửa gold sau khi xem test**. Nếu tính bằng chứng tương đương, Hit@1 test của C là 4/6, của B là 3/6, Evidence Hit@3 test của B là 5/6. Bài học: chunk gắn chặt với một trang làm đứt câu ở ranh giới trang, và gold chỉ ghi một hai trang thì bỏ sót bằng chứng hợp lệ.
- **Chiến lược chọn, đánh đổi, điều kiện áp dụng:** chọn **C** theo tiêu chí đã chốt (bằng B ở dev Evidence Hit@3 = 20/20, hơn B ở dev Hit@1 15/20 so với 14/20). Kết quả test cùng chiều: Hit@1 3/6, Evidence Hit@3 5/6, grounding 1,83. Đánh đổi: (1) C cần biết chương **trước khi** truy xuất; nếu người dùng không cho biết hoặc cho sai, filter loại mất câu trả lời đúng; (2) chunker B dựa vào heuristic riêng cho bố cục OpenStax (callout viết hoa, footer), muốn dùng cho tài liệu khác phải viết lại; (3) chi phí và độ trễ A/B/C gần như bằng nhau ở quy mô 220 chunk, nên lựa chọn này không đánh đổi tài nguyên. Điều kiện áp dụng: tài liệu có cấu trúc chương rõ, cùng thuật ngữ dùng khác nghĩa giữa các chương, và có ngữ cảnh chương từ người dùng.
- **Hạn chế:**
  - **Mẫu nhỏ:** test chỉ 6 câu, mỗi câu tương đương 17 điểm phần trăm; khác biệt B–C là đúng 1 câu ở cả dev lẫn test, không đủ để khẳng định C tốt hơn hẳn ngoài corpus này.
  - **Nhãn và thiên lệch:** câu hỏi do Claude soạn sau khi đọc corpus nên có thể dễ hơn câu hỏi thật. Nhãn grounding và metadata do Claude đề xuất, tác giả duyệt; người chấm biết kết quả Hit@k trước khi chấm. Chỉ có một người chấm, không đo độ đồng thuận.
  - **Rò rỉ dev → test:** các cặp q04/q23 và q06/q26 cùng dạng.
  - **Chunker B:** tách khung `CHECKPOINT` thành chunk chỉ gồm tiêu đề và link video. Coherence trang 169 của B bị 0, và các chunk này chiếm chỗ trong top-3 (q24, q25).
  - **Trích PDF:** mất thụt lề code và công thức.
  - **Metadata:** `chapter` giúp lọc và `page` + offset `start`/`end` giúp truy về đúng vị trí trong PDF. Hạn chế: `chapter` chỉ có 3 giá trị nên lọc còn thô (câu về 5.4 vẫn lẫn 5.5); chưa có `section`; `book_page` rỗng ở trang mở chương; `source` là đường dẫn local, URL gốc phải tra trong manifest.
  - **Tinh chỉnh chunker B:** các ngưỡng (`min_size` 80, gộp mảnh < 100 ký tự, nhận diện tiêu đề mục) được chỉnh khi xem ranh giới chunk ở trang 139 và 155. Việc này diễn ra sau khi đã soạn benchmark nhưng **trước mọi lần chạy truy xuất**. Trang 139 là trang gold của q14 (dev), nên có rủi ro nhỏ chunker được chỉnh thuận lợi cho câu đó; không xem trang gold nào của test.
  - **Đo đạc:** thời gian là một lần chạy, có độ trễ mạng; chi phí tính theo mức giá công bố, không đối chiếu hóa đơn.
- **Nếu làm lại hoặc mở rộng:**
  1. Gộp chunk chỉ có link (`CHECKPOINT` + URL) vào chunk nội dung kế bên, hoặc bỏ khỏi index.
  2. Cho phép chunk B nối sang trang sau khi câu bị đứt ở ranh giới trang, lưu `page_start`/`page_end`.
  3. Thêm trường `section` (4.1, 5.5, …) lấy từ heading để lọc mịn hơn chương.
  4. Thử hybrid BM25 + dense trên dev để xử lý lệch từ vựng kiểu q21.
  5. Tăng tập test, có người chấm thứ hai độc lập.
  6. Khi soạn gold, quét các trang khác có cùng ý để ghi đủ trang thay thế.

**Công cụ AI:** dùng Claude (Claude Code) để viết code pipeline, soạn nháp benchmark và đề xuất nhãn grounding/metadata. Cách kiểm tra: evidence kiểm bằng script trên PDF; nhãn coherence do tác giả tự chấm; nhãn grounding/metadata tác giả đọc lại từng trường hợp trong `test_audit.md`; mọi số liệu trong báo cáo lấy từ file kết quả trong `starter/results/`.
