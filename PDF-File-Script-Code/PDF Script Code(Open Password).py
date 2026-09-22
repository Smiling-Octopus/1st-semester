# PDF 파일에 암호를 설정하는 스크립트 코드입니다.
# 이 코드는 pypdf 라이브러리를 사용하여 PDF 파일을 암호화합니다.

from pypdf import PdfReader, PdfWriter

input_pdf = "example.pdf"
output_pdf = "protected.pdf"
password = "1234"  # 원하는 비밀번호 설정

reader = PdfReader(input_pdf)
writer = PdfWriter()

# 원본 PDF 페이지 모두 복사
for page in reader.pages:
    writer.add_page(page)

# 암호화 설정 (owner_password는 옵션으로 추가 권한 제어 가능)
writer.encrypt(user_password=password, owner_password=password, 
               use_128bit=True)

# 암호화된 PDF 저장 (확장자는 그대로 pdf)
with open(output_pdf, "wb") as f_out:
    writer.write(f_out)

print(f"'{output_pdf}' 파일이 생성되었습니다. 열 때 비밀번호가 필요합니다.")