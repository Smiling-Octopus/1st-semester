# PDF File Script Collection

이 저장소는 최신 `pypdf` 라이브러리를 활용하여 PDF 파일의 내부 구조를 수정하고, 보안 설정 및 JavaScript 액션을 삽입하는 Python 스크립트 모음입니다.

## 포함된 스크립트

### 1. PDF 암호 설정 (`PDF Script Code(Open Password).py`)
이 스크립트는 기존 PDF 파일에 비밀번호를 설정하여 권한이 없는 사용자가 파일을 열어보는 것을 방지합니다.
- **기능**: 사용자(User) 및 소유자(Owner) 비밀번호 설정, 128비트 암호화 적용.
- **출력**: 암호화된 새로운 PDF 파일 생성.

### 2. PDF 오픈 액션 리다이렉트 (`PDF Script Code(OpenAction Redirect).py`)
이 스크립트는 PDF 파일이 열릴 때 특정 웹사이트로 자동 리다이렉트되는 JavaScript 액션을 추가합니다.
- **기능**: PDF의 루트 오브젝트에 `/OpenAction`을 추가하여 파일 오픈 시 `app.launchURL` 실행.
- **기술 상세**: `DictionaryObject`와 `NameObject`를 사용하여 PDF 카탈로그 구조를 직접 수정합니다.
- **주의**: 최신 브라우저 및 보안이 강화된 PDF 뷰어에서는 실행이 제한될 수 있습니다.

### 3. PDF 단순 경고창 출력 (`PDF Script Code(Alert).py`)
이 스크립트는 PDF 파일을 열 때 사용자에게 간단한 알림 메시지를 표시합니다.
- **기능**: `app.alert` JavaScript를 `/OpenAction` 이벤트에 등록하여 팝업 메시지를 출력합니다.

### 4. PDF 뷰어 정보 출력 (`PDF Script Code(Viewer Information Alert).py`)
이 스크립트는 PDF를 열고 있는 프로그램(뷰어)의 이름과 버전 정보를 경고창으로 보여줍니다.
- **기능**: `app.viewerType`과 `app.viewerVersion` 변수를 활용하여 환경 정보를 확인합니다.
- **용도**: 다양한 PDF 뷰어 환경에서의 호환성 테스트 및 환경 식별.

### 5. PDF 뷰어 버전 체크 및 경고 (`PDF Script Code(Viewer Version Check Alert).py`)
이 스크립트는 사용자의 PDF 뷰어 버전을 검사하여 특정 조건(Adobe Reader 9.x)이 아닐 경우 호환성 경고 메시지를 표시합니다.
- **기능**: 익명 함수(IIFE) 형태의 JavaScript 로직을 통해 뷰어 버전(`app.viewerVersion`)을 정교하게 체크합니다.
- **특징**: `TextStringObject`를 사용하여 멀티라인 JavaScript 코드를 안정적으로 PDF 내부에 삽입합니다.

### 6. PDF 전체 화면 투명 링크 생성 (`PDF Script Code(Transparent Screen Link Make).py`)
이 스크립트는 PDF 페이지 전체 영역에 보이지 않는 투명한 링크 어노테이션을 추가합니다. 사용자가 페이지의 어느 곳을 클릭하더라도 지정된 웹 주소로 연결됩니다.
- **기능**: 모든 페이지의 `mediabox` 정보를 바탕으로 전체 크기를 덮는 `/Link` 어노테이션 삽입.
- **기술 상세**: `ArrayObject`, `NumberObject` 등을 사용하여 좌표를 계산하고, 테두리(`Border`)를 없애 투명하게 처리합니다.
- **용도**: 특정 랜딩 페이지로의 클릭 유도 및 브라우저 기반 상호작용 테스트.

### 7. PDF 전체 화면 투명 링크 제거 (`PDF Script Code(Transparent Screen Link Delete).py`)
이 스크립트는 PDF 페이지 전체 영역에 걸쳐 있는 투명 링크 어노테이션을 찾아 제거합니다.
- **기능**: 페이지의 `mediabox`와 일치하는 `/Link` 어노테이션을 식별하여 제거.
- **기술 상세**: 어노테이션의 `/Subtype`과 `/Rect` 값을 비교하여 전체 화면 링크 여부를 판단합니다.
- **용도**: 불필요하거나 악의적인 전체 화면 링크를 정리하여 PDF의 원래 기능을 복원합니다.

### 8. PDF PowerShell 명령어 삽입 (`PDF Script Code(Windows Powershell Script Code).py`)
이 스크립트는 PDF 파일이 열릴 때 특정 PowerShell 명령어를 실행하도록 PDF에 삽입합니다.
- **기능**: PDF의 `OpenAction`에 `/Launch` 액션을 추가하여 PDF 오픈 시 지정된 PowerShell 명령어를 실행합니다.
- **기술 상세**: `pdfrw` 라이브러리를 사용하여 `/Launch` 액션과 PowerShell 명령어를 정의하고, 이를 PDF의 루트(`Root.OpenAction`)에 할당합니다.
- **주의**: 이 기능은 보안상의 이유로 Adobe Reader 9.2 이하 버전에서만 작동하며, 최신 버전의 PDF 뷰어에서는 실행이 제한됩니다.
- **용도**: 특정 환경에서의 자동화된 작업 실행 또는 보안 취약점 테스트.


## 기술적 특징
- **Library**: 기존 `PyPDF2`의 후속 버전인 `pypdf`를 사용하여 더 나은 성능과 최신 PDF 표준 호환성을 제공합니다.
- **Multi-Library Support**: 액션 삽입의 특성에 따라 `pypdf`와 `pdfrw`를 선택적으로 활용합니다.
- **Low-level Manipulation**: `writer._root_object.update`를 통해 PDF의 루트 사전(Root Dictionary)을 직접 제어하여 표준 라이브러리 함수 이상의 커스텀 액션을 구현합니다.

## 요구 사항

스크립트를 실행하기 위해서는 Python 3.x 환경과 `pypdf`, `pdfrw` 라이브러리가 필요합니다.

```bash
pip install pypdf pdfrw
```

## 사용 방법

1. **준비**: 수정하려는 원본 PDF 파일(`example.pdf`)을 스크립트와 같은 폴더에 배치합니다.
2. **설정**: 각 스크립트 상단의 `input_pdf`, `output_pdf`, `password` 또는 `target_url` 변수를 목적에 맞게 수정합니다.
3. **실행**:
   ```bash
   python "PDF Script Code(Open Password).py"
   # 또는
   python "PDF Script Code(OpenAction Redirect).py"
   # 또는
   python "PDF Script Code(Alert).py"
   # 또는
   python "PDF Script Code(Viewer Information Alert).py"
   # 또는
   python "PDF Script Code(Viewer Version Check Alert).py"
   # 또는
   python "PDF Script Code(Transparent Screen Link Delete).py"
   # 또는
   python "PDF Script Code(Transparent Screen Link Make).py" 
   # 또는
   python "PDF Script Code(Windows Powershell Script Code).py"
   ```

## 주의 사항

- **보안**: JavaScript 리다이렉트 기능은 최신 웹 브라우저 내장 PDF 뷰어나 보안이 강화된 최신 PDF 리더기에서는 작동하지 않을 수 있습니다.
- **라이브러리**: 기존 `PyPDF2` 라이브러리의 최신 버전인 `pypdf`를 사용하므로, 구버전 설치 시 오류가 발생할 수 있습니다. 반드시 `pip install pypdf`를 통해 설치하세요.
- **법적 책임**: 이 스크립트를 사용하여 생성된 결과물에 대한 책임은 사용자 본인에게 있습니다.