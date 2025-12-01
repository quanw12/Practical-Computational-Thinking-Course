# Exercise 01: Phát Hiện Tin Giả - Kiểm Tra và Chuẩn Bị Dữ Liệu

## Tổng Quan
Báo cáo này trình bày quy trình có cấu trúc để đánh giá và xử lý dữ liệu phục vụ mô hình học máy phát hiện tin tức giả mạo, được thực hiện dựa trên notebook Kaggle mẫu.

Dataset được sử dụng có 4 thuộc tính: title (tiêu đề bài báo), text (nội dung chi tiết), subject (lĩnh vực), và date (thời gian xuất bản).

## Quy Trình Kiểm Tra và Chuẩn Bị Dữ Liệu Từng Bước

### Giai Đoạn 1: Nạp Dữ Liệu và Kiểm Tra Ban Đầu

#### 1.1 Import Các Thư Viện Cần Thiết
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import re
import string
```

**Mục đích:** Tải các thư viện cần thiết để xử lý dữ liệu (pandas, numpy), biểu diễn đồ thị (seaborn, matplotlib), thực hiện các thuật toán ML (scikit-learn), và chuẩn bị dữ liệu văn bản (re, string).

#### 1.2 Nạp Dữ Liệu
```python
df_fake = pd.read_csv("../input/fake-news-detection/Fake.csv")
df_true = pd.read_csv("../input/fake-news-detection/True.csv")
```

**Cách Kiểm Tra Dữ Liệu:**
- `df_fake.head()` - Xem 5 hàng đầu để nắm cấu trúc dữ liệu
- `df_fake.shape` - Kích thước dataset tin giả: (23481, 4)
- `df_true.shape` - Kích thước dataset tin thật: (21417, 4)

**Nhận Định:**
- Hai dataset có cùng cấu trúc cột
- Dataset tin giả nhiều hơn khoảng 2,000 mẫu
- Dữ liệu có format đồng nhất và sạch sẽ

### Giai Đoạn 2: Kỹ Thuật Tạo Đặc Trưng Mục Tiêu

#### 2.1 Tạo Nhãn Phân Loại Nhị Phân
```python
df_fake["class"] = 0
df_true["class"] = 1
```

**Giải thích:** Tạo biến nhị phân để đánh dấu loại tin:
- `0` = tin giả
- `1` = tin thật

Bước này hợp nhất hai dataset thành một bài toán phân loại.

#### 2.2 Dành Riêng Dữ Liệu Cho Kiểm Tra Thủ Công
```python
df_fake_manual_testing = df_fake.tail(10).copy()
df_true_manual_testing = df_true.tail(10).copy()

# Xóa các bản ghi này khỏi dữ liệu huấn luyện
for i in range(23480, 23470, -1):
    df_fake.drop([i], axis=0, inplace=True)
```

**Mục đích:** Trích 20 mẫu (10 tin giả, 10 tin thật) làm bộ test thủ công, phục vụ kiểm thử sau khi huấn luyện và đảm bảo đánh giá công bằng.

### Giai Đoạn 3: Hợp Nhất Dataset

#### 3.1 Gộp Các Dataset
```python
df_merge = pd.concat([df_fake, df_true], axis=0)
```

**Kết quả:** Dataset đã gộp có 44,878 bản ghi tổng cộng (23,471 tin giả + 21,407 tin thật).

#### 3.2 Lựa Chọn Đặc Trưng
```python
df = df_merge.drop(["title", "subject", "date"], axis=1)
```

**Lý Do Bỏ Các Đặc Trưng:**
- **Title**: Có thể chứa câu click-bait gây nhiễu.
- **Subject**: Chỉ là nhóm chủ đề, không có giá trị phân loại.
- **Date**: Không liên quan đến nội dung văn bản.

**Đặc Trưng Sử Dụng:**
- **text**: Nội dung chính của bài báo
- **class**: Nhãn phân loại (nhị phân)

### Giai Đoạn 4: Đánh Giá Chất Lượng Dữ Liệu

#### 4.1 Phát Hiện Giá Trị Thiếu
```python
df.isnull().sum()
```

**Kết quả:**
```
text     0
class    0
```

**Giải thích:** Không có giá trị thiếu, nên không cần thay thế.

### Giai Đoạn 5: Ngẫu Nhiên Hóa Dữ Liệu

#### 5.1 Xáo Trộn Các Bản Ghi
```python
df = df.sample(frac=1)
df.reset_index(inplace=True)
df.drop(["index"], axis=1, inplace=True)
```

**Lý Do Quan Trọng:**
- **Tránh thiên lệch**: Dữ liệu gốc theo thứ tự thời gian nên cần xáo trộn
- **Phân chia công bằng**: Train/test phân bổ ngẫu nhiên giúp đánh giá chính xác
- **Hội tụ tốt hơn**: Thứ tự ngẫu nhiên giúp gradient descent ổn định

### Giai Đoạn 6: Tiền Xử Lý Văn Bản

#### 6.1 Hàm Làm Sạch Văn Bản Tùy Chỉnh
```python
def wordopt(text):
    text = text.lower()                                              # Chuẩn hóa chữ thường
    text = re.sub('\[.*?\]', '', text)                               # Xóa dấu ngoặc vuông và nội dung
    text = re.sub("\\W", " ", text)                                  # Thay thế ký tự không phải từ
    text = re.sub('https?://\S+|www\.\S+', '', text)                 # Xóa URLs
    text = re.sub('<.*?>+', '', text)                                # Xóa thẻ HTML
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)  # Xóa dấu câu
    text = re.sub('\n', '', text)                                    # Xóa ký tự xuống dòng
    text = re.sub('\w*\d\w*', '', text)                              # Xóa từ chứa số
    return text
```

**Lý Do Tiền Xử Lý:**

|        Thao Tác         |                   Mục Đích                  |               Ví Dụ               |
|-------------------------|---------------------------------------------|-----------------------------------|
| Chuyển thành chữ thường | Đảm bảo khớp không phân biệt chữ hoa/thường | "Trump" → "trump"                 |
| Xóa URL                 | Loại bỏ các liên kết không mang thông tin   | "Visit www.example.com" → "Visit" |
| Xóa dấu câu             | Giảm kích thước từ vựng                     | "Hello!" → "Hello"                |
| Xóa số                  | Loại bỏ nhiễu thời gian/số                  | "2017 election" → "election"      |

#### 6.2 Áp Dụng Tiền Xử Lý
```python
df["text"] = df["text"].apply(wordopt)
```

**Mục đích:** Chuẩn hóa văn bản thô thành dạng dùng được cho thuật toán học máy.

### Giai Đoạn 7: Phân Chia Train-Test

#### 7.1 Tách Đặc Trưng và Mục Tiêu
```python
x = df["text"]
y = df["class"]
```

#### 7.2 Phân Vùng Dữ Liệu
```python
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
```

**Tham số:**
- **Test set**: 25%

### Giai Đoạn 8: Vector Hóa Đặc Trưng

#### 8.1 Biến Đổi TF-IDF
```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)
```

**TF-IDF (Term Frequency-Inverse Document Frequency):**
- **TF**: Đếm tần suất từ trong mỗi bài
- **IDF**: Giảm trọng số các từ phổ biến
- **Kết quả**: Mã hóa văn bản thành vector số

**Nguyên tắc:**
- **Fit trên train**: Học vocabulary từ dữ liệu huấn luyện
- **Transform trên test**: Áp dụng vocabulary đã học
- **Tránh data leakage**: Đảm bảo test không ảnh hưởng quá trình học

## Kết Luận

Đây là cách tiếp cận có hệ thống và mang tính khoa học để xử lý dữ liệu cho bài toán NLP. Quá trình này chuyển dữ liệu văn bản thô sang định dạng sẵn sàng học bằng các bước: kiểm định chất lượng, làm sạch, xử lý và vector hóa. Độ chính xác 98.5% (Logistic Regression) và 99.6% (Decision Tree) cho thấy quy trình xử lý dữ liệu hiệu quả.

Nhìn chung, **xử lý dữ liệu chiếm khoảng 80% công sức**, và cẩn thận trong kiểm định chất lượng, tiền xử lý và chia dữ liệu đúng cách quyết định hiệu năng và khả năng tổng quát hóa của mô hình.

***------------------------------------------------------------------------------------------------------------------------***
# Exercise 02: File Format Selection Analysis

## Câu hỏi: Bạn nên chọn định dạng tệp nào? Tại sao?

### Phân Tích Chi Tiết Các Định Dạng Tệp

#### 1. CSV (Comma-Separated Values)
**Định nghĩa:** CSV là định dạng văn bản thuần túy dùng cho dữ liệu dạng bảng, mỗi dòng là một bản ghi và các giá trị được phân cách bằng dấu phẩy.

**Ưu điểm:**
- **Đơn giản và phổ biến:** Dễ đọc và viết, tương thích với Excel, Google Sheets và thư viện pandas
- **Kích thước nhỏ:** Format gọn nhẹ giúp tiết kiệm dung lượng
- **Xử lý nhanh:** Cấu trúc đơn giản nên đọc/ghi nhanh
- **Tương thích đa nền tảng:** Hầu hết ngôn ngữ lập trình đều hỗ trợ

**Nhược điểm:**
- **Cấu trúc đơn giản:** Không mô tả được dữ liệu lồng nhau hoặc phân cấp
- **Thiếu metadata:** Không có cách chuẩn để mã hóa kiểu dữ liệu
- **Vấn đề ký tự đặc biệt:** Khó xử lý khi dữ liệu chứa dấu phân cách, xuống dòng, hoặc trích dẫn
- **Không có schema validation:** Khó đảm bảo tính nhất quán dữ liệu

**Trường hợp sử dụng:**
- Xuất/nhập dữ liệu giữa database và bảng tính
- Báo cáo tài chính và phân tích bán hàng đơn giản
- Dữ liệu khoa học dạng bảng
- Workflow phân tích với pandas hoặc R

**Ví dụ:**
id,name,age,email
1,Nguyen Van A,20,nva@example.com
2,Tran Thi B,21,ttb@example.com

#### 2. JSON (JavaScript Object Notation)
**Định nghĩa:** JSON là định dạng trao đổi dữ liệu nhẹ, vừa dễ đọc cho con người vừa dễ parse cho máy, sử dụng cú pháp object và array của JavaScript.

**Ưu điểm:**
- **Hỗ trợ cấu trúc phức tạp:** Mô tả được dữ liệu lồng nhau, mảng và phân cấp đối tượng
- **Kiểu dữ liệu rõ ràng:** Hỗ trợ string, number, boolean, null, array và object
- **Phổ biến trong Web APIs:** Chuẩn de facto cho RESTful API
- **Dễ đọc:** Pretty-printing hỗ trợ debug
- **Hỗ trợ schema validation:** Tương thích JSON Schema

**Nhược điểm:**
- **Kích thước lớn:** Nhiều ký tự overhead (brackets, quotes, commas)
- **Cần load toàn bộ:** Khó xử lý file JSON rất lớn do phải parse toàn bộ vào memory
- **Không tối ưu streaming:** Cần truyền toàn bộ file trước khi parse
- **Hiệu năng kém:** Chậm hơn định dạng binary

**Trường hợp sử dụng:**
- Request/response payload của RESTful API
- File cấu hình (package.json, settings.json)
- Dữ liệu phân cấp (user profile, product catalog)
- Hệ thống NoSQL (MongoDB, CouchDB)
- Web app và SPA

**Ví dụ:**
{
  "users": [
    {
      "id": 1,
      "name": "Nguyen Van A",
      "age": 20,
      "email": "nva@example.com",
      "address": {
        "city": "Ho Chi Minh",
        "district": "District 1"
      }
    },
    {
      "id": 2,
      "name": "Tran Thi B",
      "age": 21,
      "email": "ttb@example.com",
      "address": {
        "city": "Ha Noi",
        "district": "Ba Dinh"
      }
    }
  ]
}

#### 3. JSONL (JSON Lines / Newline-delimited JSON)
**Định nghĩa:** JSONL là định dạng text-based, mỗi dòng là một JSON object độc lập, các dòng được phân cách bằng newline.

**Ưu điểm:**
- **Hỗ trợ streaming:** Xử lý từng dòng mà không cần load toàn bộ file
- **Thêm dữ liệu dễ dàng:** Dễ thêm mới vào cuối file
- **Tiết kiệm memory:** Chỉ load một bản ghi vào memory mỗi lần
- **Xử lý song song:** Cấu trúc độc lập từng dòng, dễ parallelize
- **Chịu lỗi tốt:** Lỗi ở một dòng không ảnh hưởng dòng khác

**Nhược điểm:**
- **Ít được hỗ trợ:** Kém phổ biến hơn CSV hoặc JSON
- **Khó đọc trực tiếp:** Không có pretty-printing
- **Cần tool chuyên dụng:** Cần editor/viewer hỗ trợ JSONL
- **Thiếu cấu trúc tổng:** Không có array wrapper cho dataset

**Trường hợp sử dụng:**
- Log file và hệ thống event streaming
- Dataset học máy (training data)
- ETL pipeline và xử lý dữ liệu
- Ứng dụng big data (Apache Spark, Hadoop)
- Hệ thống ingestion real-time
- Export database hàng triệu bản ghi

**Ví dụ:**
{"id": 1, "name": "Nguyen Van A", "age": 20, "email": "nva@example.com"}
{"id": 2, "name": "Tran Thi B", "age": 21, "email": "ttb@example.com"}
{"id": 3, "name": "Le Van C", "age": 22, "email": "lvc@example.com"}

### Kết Luận và Khuyến Nghị
**Quan điểm chính:** Mỗi định dạng phục vụ mục đích khác nhau, việc chọn phụ thuộc vào nhiều yếu tố:

1. **Độ phức tạp cấu trúc dữ liệu:**
   - Dữ liệu bảng đơn giản → CSV
   - Dữ liệu phân cấp → JSON hoặc JSONL

2. **Kích thước dataset:**
   - Nhỏ đến trung bình (< 100MB) → CSV hoặc JSON
   - Dataset lớn (> 100MB) → JSONL

3. **Phương pháp xử lý:**
   - Batch processing → CSV hoặc JSON
   - Streaming/Real-time → JSONL
   - Giao tiếp API → JSON

4. **Yêu cầu hiệu năng:**
   - Báo cáo đơn giản → CSV
   - Truy vấn phức tạp → JSON
   - Xử lý big data → JSONL

5. **Yêu cầu tương thích:**
   - Tích hợp Excel/Spreadsheet → CSV
   - Web APIs → JSON
   - Data pipelines → JSONL

**Khuyến nghị thực tế:**
- **Cho phân tích và báo cáo:** Dùng CSV vì đơn giản và tương thích Excel, pandas
- **Cho web dev và APIs:** Dùng JSON như chuẩn industry
- **Cho ML và big data:** Dùng JSONL cho dataset quy mô lớn
- **Trong thực tế:** Nhiều hệ thống production dùng hybrid, chọn định dạng theo từng module

### Tổng Kết
Việc chọn định dạng file không phải về ưu việt tuyệt đối mà về sự phù hợp theo ngữ cảnh. Kỹ sư phần mềm cần nắm ưu/nhược của từng định dạng để quyết định cân bằng hiệu năng, bảo trì và khả năng mở rộng.