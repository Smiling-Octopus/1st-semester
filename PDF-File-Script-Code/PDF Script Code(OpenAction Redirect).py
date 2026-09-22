# 이 코드를 통해서 제작된 PDF 파일은 Adobe Reader 9.2 이하의 버전에서 동작합니다.

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, create_string_object

# 설정 값
input_pdf = "example.pdf"       # 원본 PDF 파일명
output_pdf = "redirect_pdf.pdf" # 결과 PDF 파일명
target_url = "https://google.com" # 이동시키고 싶은 주소

try:
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # 1. 모든 페이지 복사
    for page in reader.pages:
        writer.add_page(page)

    # 2. 자바스크립트 액션 생성
    # app.launchURL(url, newWindow) 함수를 사용합니다.
    # true는 새 창에서 열기, false는 현재 창(지원할 경우)에서 열기입니다.
    js_script = f"app.launchURL('{target_url}', true);"
    
    js_dict = DictionaryObject()
    js_dict.update({
        NameObject("/S"): NameObject("/JavaScript"),
        NameObject("/JS"): create_string_object(js_script)
    })

    # 3. PDF 루트에 OpenAction(열 때 실행) 등록
    writer._root_object.update({
        NameObject("/OpenAction"): js_dict
    })

    # 4. 파일 저장
    with open(output_pdf, "wb") as f_out:
        writer.write(f_out)

    print(f"성공: '{output_pdf}' 파일이 생성되었습니다.")
    print(f"설정된 URL: {target_url}")

except FileNotFoundError:
    print(f"오류: '{input_pdf}' 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"오류 발생: {e}")
