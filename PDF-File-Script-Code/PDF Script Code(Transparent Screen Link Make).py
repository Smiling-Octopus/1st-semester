from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, TextStringObject, ArrayObject, NumberObject

def add_fullscreen_transparent_link(input_pdf, output_pdf, target_url):
    try:
        # PDF 읽기 및 쓰기 준비
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            mbox = page.mediabox  # 페이지 크기 가져오기
            
            # 투명 링크 어노테이션 생성 (페이지 전체 영역)
            link_annot = DictionaryObject({
                NameObject("/Type"): NameObject("/Annot"),
                NameObject("/Subtype"): NameObject("/Link"),
                NameObject("/Rect"): ArrayObject([
                    NumberObject(mbox.left), NumberObject(mbox.bottom),
                    NumberObject(mbox.right), NumberObject(mbox.top)
                ]),
                NameObject("/A"): DictionaryObject({
                    NameObject("/S"): NameObject("/URI"),
                    NameObject("/URI"): TextStringObject(target_url)
                }),
                NameObject("/Border"): ArrayObject([NumberObject(0), NumberObject(0), NumberObject(0)])  # 테두리 없음
            })

            # 어노테이션 리스트 없으면 생성 후 링크 추가
            if "/Annots" not in page:
                page[NameObject("/Annots")] = ArrayObject()
            page[NameObject("/Annots")].append(link_annot)
            
            writer.add_page(page)  # 페이지 추가

        # 수정된 PDF 저장
        with open(output_pdf, "wb") as f_out:
            writer.write(f_out)
            
        print(f"성공: '{output_pdf}' 파일이 생성되었습니다.")

    except FileNotFoundError:
        print(f"오류: '{input_pdf}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    input_file = "example.pdf"
    output_file = "browser_linked.pdf"
    target_url = "http://192.168.0.1:8080/index.html"

    add_fullscreen_transparent_link(input_file, output_file, target_url)