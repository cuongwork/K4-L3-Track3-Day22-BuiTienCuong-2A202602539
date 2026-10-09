# Báo cáo kết quả Lab 22

**Bùi Tiến Cường — MSSV 2A202602539 — K4, Track 3**
Môi trường: Google Colab, Tesla T4. Ngày thực hiện: 08–09/10/2026.

## Mục tiêu và quy trình

Thực hiện NB0–NB4 theo hướng dẫn: tự cài DPO loss, SFT tiếng Việt, chia preference theo prompt không trùng nhau, huấn luyện DPO trên SFT đã gộp và đánh giá SFT so với SFT+DPO. Bài phản tư chi tiết theo đúng các mục của mẫu nằm trong [REFLECTION.md](REFLECTION.md).

SFT dùng 1.000 mẫu, một epoch, 125 bước. DPO dùng 800 cặp train và 100 held-out, β=0,1, lr=5e-6, LoRA r=16, một epoch, 100 bước. NB4 sinh đủ 8 prompt cố định và 50 prompt held-out với cùng cấu hình greedy cho hai mô hình.

## Kết quả chính

| Chỉ số | Kết quả |
|---|---:|
| SFT loss trung bình | 1,3602 |
| DPO loss trung bình | 0,675113 |
| Reward chosen / rejected held-out | 0,407970 / 0,319731 |
| Margin / accuracy held-out | 0,088239 / 66% |
| DPO win rate NB4 held-out, CI 95% | 47% [40%; 54%] |
| Win rate trên cặp gần bằng độ dài | 50% (45 cặp) |
| Độ dài đầu ra held-out SFT → DPO | 659,08 → 625,48 ký tự |

Reward của cả chosen và rejected tăng, chosen tăng nhiều hơn. Không diễn giải nhãn INTENDED thành rejected giảm. CI win rate chứa 50%, nên chưa có bằng chứng DPO tốt hơn SFT về chất lượng sinh. RM Qwen3 chỉ đúng 8/12 sanity và bị loại; RM Llama đúng 12/12 được dùng trong tổng hợp. Các lỗi thẻ `</tool_call>` và tuân thủ số câu vẫn tồn tại.

## Thí nghiệm bonus

- **Quét β:** cùng 800/100 cặp, β=0,05 / 0,1 / 0,5 cho accuracy 67% / 66% / 71%. Margin có hệ số β nên không dùng margin thô để xếp hạng chất lượng. Số liệu và phân tích nằm ở REFLECTION §5.
- **GGUF:** nạp và gộp 504 tensor LoRA DPO vào SFT rồi xuất Q4_K_M, dung lượng 2.497,3 MB. llama-cpp chạy được prompt Bubble Sort; nội dung gần HF nhưng cùng còn lỗi định dạng. Metadata tại `data/eval/deploy_meta.json`, ảnh chụp trực tiếp Colab tại `screenshots/06-gguf-smoke.png`.
- **Năm biến thể:** đã chạy xong DPO, RPO, DPO-norm, LD-DPO và ORPO trên cùng 300 cặp train / 100 held-out / 20 prompt sinh. Accuracy lần lượt 72% / 67% / 64% / 56% / 65%; độ dài 433,25 / 452 / 430 / 471,7 / 361,2 ký tự. LD-DPO dài nhất; ORPO ngắn nhất. Bảng và giới hạn diễn giải ở REFLECTION §8, ảnh `screenshots/03b-variants.png`.

## Bằng chứng và cách nộp

Notebook core có output: `colab/Lab22_BuiTienCuong_2A202602539_T4.ipynb`. Bốn ảnh bắt buộc nằm trong `submission/screenshots/`; JSON NB4 ở `data/eval/`; config, fingerprint và metrics DPO ở `adapters/dpo/`. Các kết quả bonus lưu tách riêng.

Verifier đã chạy thành công tại `/content/lab22` trên Colab. Adapter giữ nguyên đường dẫn reference của môi trường huấn luyện; bản chuyển sang Windows không tự đổi đường dẫn này. Chưa xác nhận lại toàn bộ Run all từ một runtime sạch sau các lần phục hồi kernel.

Nộp URL repo public vào LMS theo README §4. Trọng số và khóa API không đưa vào Git. Không có yêu cầu nộp thêm PDF/DOCX trong repo. Thời điểm hoàn thành core là sau nửa đêm 09/10; điểm trừ muộn và điểm bonus do giảng viên quyết định.

## Nguồn log và tình trạng runtime

Colab đã lưu output hoàn tất NB3b trước khi phiên GPU kết thúc. Khi kết nối lại, `/content/lab22` không còn và GPU bị giới hạn sử dụng. Các `training_log.json` bổ sung tại `adapters/dpo/`, `adapters/beta-sweep/`, `adapters/variants/` trích nguyên bảng HTML từ notebook đã lưu, giữ độ chính xác hiển thị; không phải toàn bộ log thô của trainer. Notebook kèm output gốc, không tái tạo output huấn luyện. Trọng số phiên Colab không được thu hồi; muốn chạy lại cần tạo SFT và adapter theo notebook.
