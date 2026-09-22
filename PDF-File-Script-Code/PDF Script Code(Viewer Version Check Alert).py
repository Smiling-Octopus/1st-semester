from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, TextStringObject, create_string_object

input_pdf = "example.pdf"   # alert 액션을 추가할 PDF 파일 경로
output_pdf = "alert_pdf.pdf"    # 자바스크립트 액션이 추가된 PDF 파일 경로

reader = PdfReader(input_pdf)
writer = PdfWriter()

# 모든 페이지 복사
for page in reader.pages:
    writer.add_page(page)

# JavaScript 코드로 PDF 열 때 호환성 경고 메시지 표시
# (Adobe Reader 9.2 이하 버전에서 작성된 파일임을 알리는 메시지)
js_logic = """
(function() {
    var v = app.viewerVersion.toString();
    var varName = app.viewerVariation;
    if (varName === 'Reader' && v.indexOf('9.') === 0) {
        return;
    }
    var fn = "alert";
    var msg = "하위 버전에서 작성된 파일입니다. 정상적인 열람을 위해 Adobe Reader 9.2 버전에서 실행하십시오.";
    app[fn]({ cMsg: msg, cTitle: "호환성 경고", nIcon: 0 });
})();
"""

js_action = DictionaryObject({
    NameObject("/S"): NameObject("/JavaScript"),
    NameObject("/JS"): TextStringObject(js_logic)
})

writer._root_object.update({ NameObject("/OpenAction"): js_action })

with open(output_pdf, "wb") as f_out:
    writer.write(f_out)

print(f"{output_pdf} 생성 완료")
