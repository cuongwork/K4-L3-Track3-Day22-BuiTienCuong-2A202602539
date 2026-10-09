# Đối chiếu yêu cầu nộp Lab 22

Họ tên: Bùi Tiến Cường — MSSV: 2A202602539.

Bản lõi đã push: `559460f` (09/10/2026 01:33:19 +07:00). Repo public, nhánh main. Đây là tự kiểm tra bằng chứng, không phải điểm giảng viên chấm.

| Phần | Điểm tối đa | Bằng chứng |
|---|---:|---|
| NB0 | 10 | Notebook có assert loss và giải thích likelihood displacement trong REFLECTION |
| NB1 | 8 | Output train/merge SFT, ảnh loss, config mô hình đã gộp |
| NB2 | 12 | 800/100 cặp, kiểm tra chia theo prompt, 3 cặp mẫu, ảnh và thống kê độ dài |
| NB3 | 24 | Config trỏ tới SFT của phiên Colab, metrics và đồ thị chosen/rejected của train/held-out, phân tích §3 |
| NB4 | 16 | 8 câu cố định + 50 held-out, fingerprint khớp, hai RM, sanity, CI và kiểm soát độ dài |
| Phản tư | 20 | §3: 357 từ, §4: 615 từ, §6: 291 từ; số liệu từ lần chạy thực tế |
| Tái lập | 5 | Source đã kiểm tra cú pháp; chưa xác nhận lại toàn bộ Run all trên một phiên sạch sau các lần phục hồi kernel |
| Verify | 5 | Đã chạy trên Colab `/content/lab22`: Core checks passed, exit code 0 |

## Cách kiểm tra

Notebook có output: `colab/Lab22_BuiTienCuong_2A202602539_T4.ipynb`.
Các ảnh bắt buộc nằm trong `submission/screenshots/`; phân tích trong `submission/REFLECTION.md`.
Trọng số lớn được lưu trong phiên Colab, không đưa vào Git; repo giữ config và kết quả nhỏ để chấm.

Adapter config giữ nguyên đường dẫn huấn luyện `/content/lab22/models/sft-merged`.
`scripts/verify.py` so đường dẫn tuyệt đối nên bản tải về Windows báo WRONG REF dù dữ liệu và config không thay đổi.
Muốn kiểm tra đúng môi trường gốc, chạy `python scripts/verify.py` tại `/content/lab22` sau khi tạo các artifact trong Colab.
Không sửa config hoặc nới điều kiện verifier để che lỗi di chuyển đường dẫn.

## Hình thức nộp theo README §4

- Nộp URL repo public vào LMS: https://github.com/cuongwork/K4-L3-Track3-Day22-BuiTienCuong-2A202602539
- Hướng dẫn trong repo không cung cấp URL form riêng. Chưa kiểm tra giao diện LMS hoặc xác nhận đã bấm nộp trên LMS.
- Giữ repo public đến khi có điểm. Chỉ artifact đã commit được tính; file còn trong Colab hoặc Downloads chưa đủ.
- Không có yêu cầu nộp PDF, DOCX hay ZIP lên LMS. ZIP là phương tiện tải kết quả từ Colab về để đưa vào repo.
- Không commit trọng số, `.env` hoặc khóa API. Theo danh sách cho phép trong `.gitignore`, giữ các JSON cấu hình, split, metrics và training log nhỏ.

## Artifact bản cuối

| Artifact | Trạng thái |
|---|---|
| Colab NB0–NB4 và bonus có output | Notebook kết hợp có output thực; NB3b có dòng `NB3b COMPLETE` |
| 4 ảnh core, ảnh β, ảnh 5 biến thể | Đủ file; ảnh NB3b lấy trực tiếp output PNG của Colab |
| `06-gguf-smoke.png` | Ảnh chụp trình duyệt thật, có cell GGUF/Q4_K_M và câu trả lời |
| `REFLECTION.md`, `REPORT.md` | Đã cập nhật số liệu thực, bảng 5 biến thể và phân tích độ dài |
| Training log JSON | Bảng log HTML được trích từ notebook, có provenance và độ chính xác hiển thị; không phải toàn bộ log thô |
| β sweep (+6), GGUF (+4), 5 biến thể (+8) | Đã có output, số liệu, ảnh và phân tích; điểm do giảng viên chấm |
| Runtime/trọng số | Phiên GPU đã kết thúc, GPU hết hạn mức; không còn artifact runtime để thu hồi log thô/trọng số |
| Tái lập sạch | Đã loại phụ thuộc file upload khỏi source notebook; chưa chạy lại toàn bộ trên runtime sạch |
| LMS | Người học nộp URL repo public; chưa xác nhận nộp trên LMS |

Notebook cuối giữ output thực đã lưu, đồng bộ helper/source và phản tư để chạy lại; bỏ hai cell vận chuyển ảnh/xuất artifact chưa chạy. Không chỉnh hay tạo lại output để giả bằng chứng. `BONUS-CHALLENGE.md` là thử thách riêng không chấm điểm. Điểm trừ muộn do giảng viên quyết định.
