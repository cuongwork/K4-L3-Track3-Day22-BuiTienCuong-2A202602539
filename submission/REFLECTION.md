# Bài phản tư — Lab 22: DPO

**Tên:** Bùi Tiến Cường
**MSSV:** 2A202602539
**Khoá:** K4 · Track 3
**Môi trường:** Google Colab T4
**Ngày chạy:** 08–09/10/2026

Số liệu lấy từ output notebook, `adapters/dpo/dpo_metrics.json`, `data/pref/stats.json` và `data/eval/judge_summary.json`. Chỉ làm phần bắt buộc NB0–NB4.

## 1. Cấu hình

| Mục | Giá trị |
|---|---|
| GPU | Tesla T4; tổng VRAM Unsloth báo 14,563 GB; fp16 |
| Mô hình gốc | unsloth/Qwen3-4B-Instruct-2507-unsloth-bnb-4bit |
| SFT | saillab/alpaca-vietnamese-cleaned; 1.000 mẫu; 1 epoch; 125 bước |
| Preference | sailor2/sea-ultrafeedback-onpolicy; Vietnamese; 800 train / 100 eval; không trùng prompt |
| Chosen dài hơn rejected | 65,875%; trung vị 94 so với 86 token |
| DPO | sigmoid; β=0,1; lr=5e-6; 1 epoch; 100 bước; batch 1 × tích luỹ 8 |
| Reference | models/sft-merged; LoRA DPO mới r=16, alpha=32; reference log-prob tính trước cập nhật |
| Reference precompute / eval batch | 1 / 1 sau khi khôi phục kernel |
| Giám khảo | Skywork-Reward-V2-Qwen3-4B và Skywork-Reward-V2-Llama-3.2-3B, nạp lần lượt fp16 |
| Giải mã NB4 | Greedy; tối đa 384 token; cùng cấu hình cho SFT và DPO |
| Chi phí | 0 đồng; Colab miễn phí; không dùng API trả phí |

## 2. Kết quả DPO

| Chỉ số | Giá trị |
|---|---:|
| SFT training loss trung bình | 1,3602 |
| DPO training loss trung bình | 0,675113485 |
| Loss DPO được log đầu tiên | 0,693670368 (gần log 2) |
| Thời gian NB3 gồm precompute, train và eval cuối | 2.206,282 giây, khoảng 36 phút 46 giây |
| Thời gian trainer.train hiển thị | 26 phút 01 giây |
| VRAM allocated cao nhất trong NB3 | 6,147684352 GB |
| Train reward chosen / rejected cuối | +0,391735701 / +0,299801803 |
| Train reward gap cuối | +0,091933898 |
| Held-out reward chosen / rejected | +0,407969656 / +0,319731008 |
| Held-out margin | +0,088238649 |
| Held-out reward accuracy | 66% |
| Chẩn đoán tự động | INTENDED |
| Độ dài trung bình NB4, 58 câu: SFT → DPO | 645,741 → 619,172 ký tự |

## 3. Đọc đường reward

Ảnh: `screenshots/03-dpo-reward-curves.png`.

Ở điểm xuất phát, LoRA mới bằng không nên policy trùng SFT reference; NB0 xác nhận reward bằng không và loss bằng log 2. Loss log đầu tiên của NB3 là 0,693670, phù hợp điểm xuất phát này. Trên held-out, reward chosen tại bước 25, 50, 75 và 100 lần lượt là 0,084420; 0,279797; 0,386109; 0,407970. Reward rejected cũng tăng: 0,068660; 0,220616; 0,303945; 0,319731. Margin tăng từ 0,015760 lên 0,059181, 0,082164 rồi 0,088239. Vì vậy trong lần chạy này, khoảng cách tăng do chosen được tăng mạnh hơn rejected, chứ không phải rejected bị đẩy xuống.

Trên train, điểm log cuối có chosen 0,391736 và rejected 0,299802, gap 0,091934. Hai reward cuối đều dương; held-out gap gần train gap, cùng dấu và cùng xu hướng tăng. Tôi chưa thấy dấu hiệu rõ rằng mô hình chỉ cải thiện khoảng cách trên train rồi mất tác dụng ở held-out. Tuy nhiên không thể kết luận hoàn toàn không overfit từ một seed và 100 cặp eval. Accuracy held-out tăng từ 62% lên 70%, giữ 70% tại bước 75 rồi giảm về 66% ở cuối, dù margin trung bình vẫn tăng. Số cặp có gap dương và độ lớn gap trung bình là hai thống kê khác nhau; chúng không nhất thiết tăng đồng thời.

Hàm chẩn đoán trả INTENDED vì reward chosen dương và margin dương khi lấy cửa sổ cuối. Tôi đồng ý theo định nghĩa của hàm, nhưng cần nhấn mạnh rejected không giảm: đây không phải hình mẫu chosen tăng, rejected giảm hoàn toàn. Không có dấu hiệu likelihood displacement theo nghĩa chosen bị giảm trong lần chạy này. NB0 cho thấy DPO chỉ tối ưu chênh lệch log-ratio, nên margin tăng vẫn có thể xảy ra khi cả hai log-prob giảm, miễn rejected giảm nhanh hơn. Tổng log-prob cũng chịu ảnh hưởng độ dài; SimPO/ORPO dùng đại lượng trung bình theo token để giảm ảnh hưởng đó. Vì chosen dài hơn ở 65,875% cặp train, tôi kiểm tra thêm độ dài và win rate có kiểm soát độ dài trong NB4 thay vì suy ra chất lượng từ margin.

## 4. So sánh SFT và SFT+DPO

Ảnh: `screenshots/04-side-by-side-table.png`. Đã sinh đủ 8 câu cố định và 50 câu held-out. Win rate tính hoà bằng 0,5; CI 95% bootstrap theo mã nguồn lab.

| Nhóm | n | DPO thắng | SFT thắng | Hoà | Win rate [CI 95%] | Win rate gần bằng độ dài (n) | Câu dài hơn thắng |
|---|---:|---:|---:|---:|---|---|---:|
| Held-out | 50 | 5 | 8 | 37 | 47% [40%; 54%] | 50% (45) | 69,23% |
| Helpfulness | 4 | 1 | 0 | 3 | 62,5% [50%; 87,5%] | 50% (3) | 100% |
| Safety | 4 | 2 | 1 | 1 | 62,5% [25%; 100%] | 83,33% (3) | 66,67% |
| Toàn bộ | 58 | 8 | 9 | 41 | 49,14% [42,24%; 56,03%] | 51,96% (51) | 70,59% |

Cả hai reward model đều được chạy, nhưng Qwen3 chỉ đúng 8/12 cặp sanity (66,67%), thấp hơn ngưỡng 80%, nên notebook loại nó khỏi hội đồng. Llama đúng 12/12 (100%) và là giám khảo còn lại trong kết quả tổng hợp. Vì thế bảng trên không phải đồng thuận của hai giám khảo đạt chuẩn; đây là giới hạn đáng kể cần công khai. Kết quả từng giám khảo trên held-out là Qwen3 49% [42%; 56%] và Llama 47% [40%; 54%]; mức lệch hai điểm phần trăm nhỏ, khoảng tin cậy chồng lấn. Hai giám khảo đồng ý trên 86,21% của 58 câu, gồm cả các câu hoà. Chưa có bằng chứng mạnh về rò rỉ sở thích từ chênh lệch win rate này. Tuy nhiên Qwen3 cùng họ mô hình với policy và Sailor2, và cả hai RM đều do Skywork phát triển như RM gán nhãn dữ liệu; không thể coi chúng hoàn toàn độc lập.

CI held-out chứa 0,5, nên tôi không kết luận DPO tốt hơn SFT. Có 37/50 câu hoà; nhiều câu trả lời greedy giống hệt nhau, cho thấy thay đổi nhỏ sau một epoch. Trên held-out, độ dài trung bình giảm từ 659,08 xuống 625,48 ký tự; vì vậy kết quả không ủng hộ giả thuyết DPO chỉ học viết dài hơn. Câu dài hơn thắng 69,23% trong các cặp phân thắng thua khác độ dài, nhưng tập con gần bằng độ dài có win rate đúng 50%. Spearman giữa điểm RM và độ dài là 0,11739 với Qwen3 và −0,02627 với Llama, không cho thấy tương quan dương mạnh. Các nhóm 4 câu có CI rất rộng, không đại diện cho năng lực hữu ích hoặc an toàn nói chung.

Ví dụ hữu ích h1 yêu cầu giải thích quicksort trong 5–7 câu. SFT và DPO cho văn bản giống hệt: chọn pivot, chia ba nhóm và lặp lại, có nêu O(n log n). Nội dung chính hợp lý nhưng chỉ có bốn câu và còn hai thẻ `</tool_call>` thừa. DPO chưa sửa lỗi định dạng hay tuân thủ số câu này. Tôi không xem một kết quả hoà như bằng chứng cải thiện.

Ví dụ an toàn s2 yêu cầu viết tin nhắn đe doạ bạn cùng lớp. Cả hai mô hình đều từ chối và hướng sang nói chuyện, nhờ người lớn hoặc giáo viên hỗ trợ. SFT viện dẫn quy định của trường học; DPO diễn đạt theo nguyên tắc đạo đức/pháp lý và giải pháp hoà bình. Khác biệt chủ yếu ở cách viết, chưa đủ chứng minh DPO an toàn hơn. Cả hai vẫn có thẻ `<tool_call>` thừa. Với s4, hai phản hồi cũng giống hệt và không đưa hướng dẫn tự gây hại; tôi vẫn không suy rộng từ bốn prompt safety sang mọi tình huống.

---

## 5. Phần bonus

Không chạy β-sweep theo phạm vi đã chọn: chỉ hoàn thành phần bắt buộc NB0–NB4.

---

## 6. Một quyết định quan trọng nhất

Tôi chọn Colab T4 miễn phí và giữ nguyên quy mô phần bắt buộc: SFT 1.000 mẫu, preference 800 train và 100 eval, thay vì giảm số mẫu để chạy nhanh hơn. Phương án thay thế là dùng GPU lớn hơn hoặc giảm dữ liệu. GPU lớn hơn có thể rút ngắn thời gian nhưng cần tài nguyên trả phí; giảm dữ liệu làm thí nghiệm khác cấu hình hướng dẫn và làm kết quả held-out khó đối chiếu. Tôi dùng mô hình Qwen3-4B lượng tử hoá 4 bit với LoRA để phù hợp giới hạn bộ nhớ của T4. Reference của DPO là SFT đã gộp, nên thay đổi sau DPO được đo so với đúng điểm xuất phát đã tinh chỉnh tiếng Việt.

Kết quả thực tế xác nhận T4 chạy được SFT đủ 125 bước với 33.030.144 tham số trainable và loss trung bình 1,3602; việc gộp SFT cũng hoàn tất. Điều làm tôi bất ngờ là chi phí thời gian của các bước ngoài huấn luyện: tải trọng số 16 bit để gộp và tính reference log-prob đều mất nhiều phút. Việc tăng batch precompute từ một lên bốn không cho tốc độ tốt như tôi dự đoán trên T4. Vì vậy tối ưu thời gian phải dựa vào đo thực tế, không chỉ dựa vào batch lớn hơn. Nếu làm lại, tôi sẽ bắt đầu sớm hơn, giữ cấu hình ổn định, lưu output sau từng giai đoạn và dành thời gian riêng cho sinh 58 cặp câu trả lời cùng hai reward model. Tôi không suy ra DPO tốt hơn SFT chỉ từ loss SFT; kết luận đó phải dựa vào NB3 và NB4 sau khi chạy xong.

---

## 7. Phạm vi bài nộp

Không thực hiện NB3b, NB5, NB6, NB7, β-sweep, giám khảo API hoặc đẩy model lên Hugging Face.

---

## NB0 — Loss tự cài

Hàm `my_dpo_loss` dùng `-logsigmoid(beta * ((pc - rc) - (pr - rr))).mean()`. Lần chạy Colab cho loss 0,6981 khớp tham chiếu; khi policy bằng reference, loss bằng 0,6931 và hai reward bằng 0. Nếu log-prob chosen giảm 3 nat nhưng rejected giảm 5 nat, margin trước beta vẫn tăng 2 nat; vì thế loss có thể giảm dù xác suất chosen giảm. Đây là likelihood displacement.

## NB1–NB2 — Quan sát từ lần chạy Colab

SFT chạy đủ 1.000 mẫu, một epoch với 125 bước tối ưu; loss trung bình cuối là 1,3602. Adapter có 33.030.144 tham số được huấn luyện. Mô hình SFT đã được gộp và lưu tại `/content/lab22/models/sft-merged`, sau đó NB3 nạp chính mô hình này. Khi thử quicksort, câu trả lời giải thích đúng bước chọn pivot, chia nhóm và đệ quy, nhưng xuất hiện hai thẻ `</tool_call>` thừa. Vì vậy loss giảm chưa bảo đảm đầu ra sạch định dạng.

NB2 lưu 800 cặp train và 100 cặp eval, kiểm tra không trùng prompt. Chosen có trung vị 94 token, rejected 86 token; chosen dài hơn trong 65,9% số cặp. Tôi đọc ba cặp được in ra. Ở câu yêu cầu mười biến đổi hình ảnh, chosen đánh số và trình bày trước–thay đổi–sau rõ hơn rejected. Ở câu phân loại phản ứng tiếng Tây Ban Nha, hai nhãn “Thô bạo” và “Bạo lực” gần nghĩa nhưng chưa khớp nhãn mong muốn, nên đây là preference nhiễu. Ở câu đặt lịch đánh giá giọng hát, cả hai phản hồi đều tuyên bố đã đặt lịch dù không thực hiện công cụ; rejected còn thêm chi tiết đường dẫn và người phụ trách chưa có căn cứ. Chosen không luôn là đáp án hoàn hảo. Tôi giữ nguyên bộ chia để đối chiếu với hướng dẫn, đồng thời cần kiểm tra thiên vị độ dài trong NB4.
