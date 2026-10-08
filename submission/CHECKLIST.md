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

Bonus đang chạy được lưu riêng; chỉ tính sau khi đủ metrics, ảnh và phân tích rồi push.
Điểm trừ nộp muộn phụ thuộc thời điểm nộp và cách giảng viên áp dụng rubric; không suy ra điểm chính thức từ giờ commit.
