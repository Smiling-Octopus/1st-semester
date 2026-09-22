from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, ArrayObject, NumberObject

def remove_fullscreen_transparent_link(input_pdf, output_pdf):
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            mbox = page.mediabox
            if "/Annots" in page:
                annots = page[NameObject("/Annots")]
                new_annots = []

                for annot in annots:
                    subtype = annot.get("/Subtype")
                    rect = annot.get("/Rect")

                    # 기존 전체 화면 링크 어노테이션과 비교 조건:
                    # /Subtype이 /Link이면서 Rect가 페이지 크기인 경우 제외
                    is_fullscreen_link = (
                        subtype == "/Link" and
                        rect is not None and
                        len(rect) == 4 and
                        float(rect[0]) == float(mbox.left) and
                        float(rect[1]) == float(mbox.bottom) and
                        float(rect[2]) == float(mbox.right) and
                        float(rect[3]) == float(mbox.top)
                    )

                    if not is_fullscreen_link:
                        new_annots.append(annot)

                # 어노테이션 리스트 갱신 (전체화면 링크 어노테이션 제외)
                if new_annots:
                    page[NameObject("/Annots")] = ArrayObject(new_annots)
                else:
                    # 남은 어노테이션 없으면 필드 삭제
                    del page[NameObject("/Annots")]

            writer.add_page(page)

        with open(output_pdf, "wb") as f_out:
            writer.write(f_out)

        print(f"성공: '{output_pdf}' 파일에서 전체 화면 투명 링크를 제거했습니다.")

    except FileNotFoundError:
        print(f"오류: '{input_pdf}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    input_file = "browser_linked.pdf"  # 링크가 포함된 PDF
    output_file = "cleaned_example.pdf"    # 링크가 제거된 PDF

    remove_fullscreen_transparent_link(input_file, output_file)