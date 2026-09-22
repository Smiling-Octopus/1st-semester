# Windows 환경에서 PDF를 활용한 시스템 정보 수집 및 보안 실습

Windows 시스템 정보 수집 프로그램과 PDF 파일의 구조·스크립트·액션을 다루는 Python 실습 코드 저장소입니다. PDF 파일 처리, 시스템 정보 수집, 실행 파일 패키징 과정을 학습하고 각 기능의 동작과 보안상 제약사항을 확인하는 것을 목적으로 합니다.

> 본 저장소의 구현과 실험은 본인이 소유하거나 사용 권한을 받은 시스템과 문서에서만 수행해야 합니다. PDF JavaScript, `/Launch`, PowerShell 실행 액션은 격리된 테스트 환경에서만 검증하세요.

## 프로젝트 개요

이 프로젝트는 다음 두 가지 실습을 포함합니다.

1. Windows 운영체제의 시스템·네트워크 정보를 수집하여 JSON 파일로 저장하는 프로그램
2. PDF의 비밀번호, 링크 주석, OpenAction 및 JavaScript 동작을 수정·확인하는 Python 스크립트 모음

수집 프로그램은 운영체제, CPU, 메모리, 네트워크 인터페이스, 공인 IP 및 IP 기반 위치 정보를 다룹니다. PDF 스크립트는 문서 구조를 직접 수정하여 보안 설정과 PDF 뷰어 동작을 실습합니다.

## 현재 상태

기본 기능 구현이 완료된 실습 단계입니다.

- Windows 시스템 정보 수집 코드 구현
- `system_info.txt` JSON 출력 구현
- `pypdf` 기반 PDF 수정 스크립트 구현
- `pdfrw` 기반 PDF `/Launch` 액션 실습 코드 구현
- PyInstaller를 이용한 Windows 실행 파일 생성 확인

## 대상 환경

| 구분 | 환경 |
| --- | --- |
| 운영체제 | Microsoft Windows 권장 |
| 실행 환경 | Python 3.x |
| PDF 뷰어 | JavaScript 및 OpenAction 지원 여부에 따라 동작이 달라질 수 있음 |
| 테스트 환경 | 격리된 가상 환경 또는 테스트용 문서 권장 |

## 개발 환경

- Python 3.x
- PowerShell
- Visual Studio Code 등 Python 편집기
- Python 라이브러리: `pypdf`, `pdfrw`, `psutil`
- Windows용 PyInstaller

## 구현 기능

### Windows 시스템 정보 수집

`Windows-Information-Gathering/Information Gathering.py`는 다음 정보를 수집하여 `system_info.txt`에 저장합니다.

- 운영체제, 호스트명, Python 버전, 플랫폼 정보
- CPU 개수, 메모리, 스왑 메모리, 부팅 시간
- 네트워크 인터페이스, MAC 주소, IPv4/IPv6 주소, 연결 상태
- `api.ipify.org`를 통한 공인 IP
- `ipinfo.io`를 통한 IP 기반 위치 및 조직 정보

`psutil`이 설치되어 있지 않은 경우 일부 시스템·네트워크 정보만 수집합니다.

### PDF 파일 스크립트

`PDF-File-Script-Code` 폴더에는 다음 기능의 스크립트가 포함되어 있습니다.

| 스크립트 | 기능 |
| --- | --- |
| `PDF Script Code(Open Password).py` | PDF 사용자·소유자 비밀번호 설정 |
| `PDF Script Code(OpenAction Redirect).py` | PDF 열기 시 지정 URL로 이동하는 JavaScript 추가 |
| `PDF Script Code(Alert).py` | PDF 열기 시 JavaScript 알림 표시 |
| `PDF Script Code(Viewer Information Alert).py` | PDF 뷰어 종류와 버전 표시 |
| `PDF Script Code(Viewer Version Check Alert).py` | PDF 뷰어 버전 확인 및 경고 표시 |
| `PDF Script Code(Transparent Screen Link Make).py` | 페이지 전체 영역에 투명 링크 주석 추가 |
| `PDF Script Code(Transparent Screen Link Delete).py` | 페이지 전체 영역의 투명 링크 주석 제거 |
| `PDF Script Code(Windows Powershell Script Code).py` | Windows `/Launch` 액션과 PowerShell 명령 구조 실습 |

## 요구 사항 및 설치

Python 3.x가 설치된 환경에서 다음 명령으로 필요한 라이브러리를 설치합니다.

```powershell
python -m pip install pypdf pdfrw psutil
```

실행 파일을 생성하려면 PyInstaller를 추가로 설치합니다.

```powershell
python -m pip install pyinstaller
```

## 실행 방법

### Windows 시스템 정보 수집 프로그램

```powershell
cd Windows-Information-Gathering
python ".\Information Gathering.py"
```

실행이 완료되면 현재 폴더에 `system_info.txt`가 생성됩니다.

실행 파일로 변환하려면 다음 명령을 사용합니다.

```powershell
pyinstaller --onefile ".\Information Gathering.py"
```

생성된 실행 파일은 `dist` 폴더에서 확인할 수 있습니다.

### PDF 스크립트

1. 테스트용 PDF를 각 스크립트가 지정한 입력 파일명으로 준비합니다.
2. 스크립트 상단의 `input_pdf`, `output_pdf`, `password`, `target_url` 값을 목적에 맞게 수정합니다.
3. `PDF-File-Script-Code` 폴더에서 원하는 스크립트를 실행합니다.

```powershell
cd PDF-File-Script-Code
python ".\PDF Script Code(Open Password).py"
```

각 스크립트의 입력·출력 파일명은 코드에 직접 지정되어 있으므로 실행 전에 확인해야 합니다.

## 저장소 구조

```text
1st-semester/
├─ PDF-File-Script-Code/                 # PDF 파일 및 스크립트 액션 실습 코드
│  ├─ PDF Script Code(Alert).py
│  ├─ PDF Script Code(Open Password).py
│  ├─ PDF Script Code(OpenAction Redirect).py
│  ├─ PDF Script Code(Transparent Screen Link Delete).py
│  ├─ PDF Script Code(Transparent Screen Link Make).py
│  ├─ PDF Script Code(Viewer Information Alert).py
│  ├─ PDF Script Code(Viewer Version Check Alert).py
│  ├─ PDF Script Code(Windows Powershell Script Code).py
│  └─ README.md
├─ Windows-Information-Gathering/        # Windows 시스템·네트워크 정보 수집 코드
│  ├─ Information Gathering.py
│  └─ README.md
└─ README.md
```

## 보안 및 개인정보 보호

- 허가받지 않은 시스템의 정보 수집이나 제3자 PDF 변조에 사용하지 마세요.
- 시스템 정보 수집 코드는 공인 IP 및 IP 기반 위치 정보를 외부 API에 요청할 수 있습니다.
- `system_info.txt`에는 IP 주소, MAC 주소, 호스트명, 위치 정보가 포함될 수 있으므로 저장소에 커밋하지 마세요.
- PDF JavaScript 및 `/Launch` 액션은 최신 PDF 뷰어에서 차단될 수 있습니다. 보안 기능을 해제하여 우회하지 마세요.
- PDF 결과물은 원본을 복사한 뒤 생성하고, 실행 전 포함된 URL·스크립트·명령을 확인하세요.

## 라이선스

현재 저장소에 별도의 라이선스 파일이 없습니다. 코드를 재사용하거나 배포하려면 저장소 소유자에게 먼저 확인하세요.
