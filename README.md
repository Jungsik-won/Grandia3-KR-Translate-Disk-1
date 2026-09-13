<div align="center">

<img src="docs/assets/grandia3-korean-banner.svg" alt="Grandia III Korean Translation Project" width="100%" />

# Grandia3-Translate

### Grandia III 한국어화 프로젝트

**PlayStation 2 일본판 『그란디아 III』 비공식 한국어 패치**

<a href="https://github.com/Jungsik-won/Grandia3-KR-Translate-Disc-1/releases/tag/v1.1.0"><img src="https://img.shields.io/badge/Release-v1.1.0-7c3aed?style=for-the-badge" alt="Release v1.1.0" /></a>
<a href="https://github.com/Jungsik-won/Grandia3-KR-Translate-Disc-1/releases/download/v1.1.0/Grandia3_KR_Disc1_v1.1.0_0a1ec442_full.xdelta"><img src="https://img.shields.io/badge/⬇%20XDELTA%20%ED%8C%A8%EC%B9%98-2.10GB-eab308?style=for-the-badge&logo=github&logoColor=white" alt="Download xdelta patch" /></a>

</div>

<p align="center">
  <a href="#korean">🇰🇷 한국어</a> ·
  <a href="#english">🇺🇸 English</a> ·
  <a href="#japanese">🇯🇵 日本語</a>
</p>

<a id="korean"></a>

## 🇰🇷 한국어

### 프로젝트 소개

그란디아 III 일본판의 텍스트·글꼴·영상·음성 이벤트 구조를 분석하고, 한국어 번역을 실제
게임에 적용하는 비공식 팬 번역 프로젝트입니다. 추출·변환·검증 도구와 번역 자료를 재현 가능한
형태로 관리하며, 원본 게임 데이터는 저장소나 배포 파일에 포함하지 않습니다.

내부 개발 빌드와 `v0.1.x-test` 공개 시험판을 거쳐 첫 정식 배포 버전을 `v1.0.0`부터 새로
시작합니다.

### 패치 대상 원본

아래 값과 정확히 일치하는 일본판 Disc 1 ISO만 지원합니다.

| 항목 | 값 |
| --- | --- |
| 게임 | `Grandia III (Japan) (Disc 1)` |
| 플랫폼/지역 | PlayStation 2 / 일본판 |
| 원본 ISO 크기 | `4,598,890,496 bytes` |
| 원본 SHA-256 | `c588a7dada3bf7175bfe97b238b0ab4c77df6401a58d766829aec9d92f3596e8` |

다른 지역판, 다른 리비전, 이미 수정된 ISO에는 적용하지 마세요.

### 최신 정식 배포판

→ [Grandia III 한국어 패치 v1.1.0 Release](https://github.com/Jungsik-won/Grandia3-KR-Translate-Disc-1/releases/tag/v1.1.0)

| 항목 | 값 |
| --- | --- |
| 버전 | `v1.1.0` |
| 형식 | `xdelta3 3.2.0 / VCDIFF + LZMA secondary` |
| 패치 파일 | `Grandia3_KR_Disc1_v1.1.0_0a1ec442_full.xdelta` |
| 패치 크기 | `2,095,896,419 bytes` |
| 패치 SHA-256 | `9507203e585145d703d2763bd14088f531c7dec92e68e00c4bd168f4c8b6bb51` |
| 결과 ISO 크기 | `4,598,890,496 bytes` |
| 결과 ISO SHA-256 | `0a1ec442452b36f49e27794c5de475872ba9a9742f0a68a90c503deace104839` |

패치는 변경분만 담고 있으며 원본 또는 완성 ISO를 포함하지 않습니다. v1.1.0 결과 ISO는 원본과
같은 크기입니다. v1.0.0→v1.1.0 단계에서도 모든 파일 extent를 그대로 보존했으며,
CLEAN→누적판 계보에는 고정 용량 planner가 안전하게 배치한 기존 relocation 135개가 포함됩니다.

### 적용 방법

1. Release의 6개 파일을 모두 같은 폴더에 받습니다.
2. LZMA를 지원하는 `xdelta3`를 설치합니다.
3. macOS/Linux에서는 `apply_in_place_ko.sh`, Windows에서는 `apply_in_place_ko.ps1`를 실행합니다.
4. 적용기는 원본·패치·결과 ISO의 크기와 SHA-256을 자동으로 확인합니다.
5. 원본은 보존되고 별도의 `Grandia3_KR_Disc1_v1.1.0.iso`가 생성됩니다.

자세한 명령과 체크섬은 Release의 `README_ko.md`와 `SHA256SUMS.txt`를 확인하세요. 결과 ISO가
4GB를 넘으므로 FAT32에는 저장할 수 없으며, 약 5GB 이상의 추가 여유 공간이 필요합니다.

### v1.1.0 주요 반영 범위

- 필드 이동 튜토리얼의 검색 버튼 빈칸을 `□` 아이콘으로 수정
- GRM10 영상 자막 17개를 음성 기준으로 전체 재동기화하고 원본 음성 보존
- v1.0.0의 누적 시스템·아이템·전투·시나리오·카지노·비행·렌더링 이벤트 자막 유지

### v1.0.0 누적 반영 범위

- 누적 시스템·상태·아이템·전투·시나리오 한국어화
- 필드/마을 아이템 입수 이름과 용량 초과 메시지 교정
- 전투 명령·작전 패널·도움말·스킬 체득 팝업 교정
- 카지노 UI와 선상/비행 대화 문맥·글리프 교정
- 비행기 메뉴 실행 흐름과 고정 레이아웃 수정, 선택지를 `비행하기`로 정리
- 비행 일반/특수 목적지 안내 페이지 교정
- 렌더링 이벤트 자막 66개 경로·58페이지, stream `0x94`·`0x95` 포함
- 누적 한국어 하드서브 영상과 GRM20 초반 누락 자막 복원
- 원본과 같은 ISO 크기, 마지막 A28→v1.0.0 단계의 파일 extent 보존·relocation 0

### 검증 상태와 실행 주의사항

정확한 CLEAN 원본에서 xdelta를 역적용해 목표 ISO의 SHA-256과 전체 byte 비교가 일치함을
확인했습니다. ISO9660/UDF 역추출, 독립 7-Zip 역추출, 핵심 파일 상속, GRM10 원본 음성 보존도
검증했습니다. 누적 기능은 개발 과정에서 반복 실기 확인했으나, v1.1.0의 검색 버튼과 GRM10
재동기화 조합은 정적 검증 완료 후 사용자 실기 확인 대기 상태입니다.

처음 실행할 때는 PCSX2를 완전히 종료하고 새 ISO로 cold boot하세요. 구 ISO에서 만든 상태저장은
사용하지 말고 일반 메모리카드 저장을 불러온 뒤 새 상태저장을 만드세요.

### 저장소 구성

| 경로 | 역할 |
| --- | --- |
| `data/` | 번역 원문·번역문·글리프·codebook 데이터 |
| `exports/` | 세션별 표준 CSV와 검토용 export |
| `tools/` | 추출·변환·빌드·검증 도구 |
| `docs/` | 세션 지침·분석 기록·릴리스 문서 |
| `translation.db` | 중앙 Translation Manager 데이터베이스 |

문제를 발견하면 GitHub Issues에 실행 환경, 원본 SHA-256, 장면/메뉴/전투 상황, 가능하면 화면
캡처와 세이브 위치를 남겨 주세요.

### 저작권 및 면책

Grandia III와 관련된 게임명, 로고, 캐릭터 및 게임 데이터의 권리는 각 권리자에게 있습니다.
이 프로젝트는 비공식·비상업적 팬 번역/연구 프로젝트이며 권리자와 제휴하거나 승인받지 않았습니다.
원본 또는 패치된 ISO를 제공하지 않으며, 사용자는 합법적으로 보유한 정확한 원본에만 패치를
적용해야 합니다. 사용으로 인한 데이터 손실이나 호환성 문제를 보증하지 않습니다.

<a id="english"></a>

## 🇺🇸 English

Grandia3-Translate is an unofficial Korean fan-translation project for the Japanese PlayStation 2
release of *Grandia III*. The first stable release starts at `v1.0.0`, following the internal
development builds and public `v0.1.x-test` releases.

### Supported source and output

- Source: `Grandia III (Japan) (Disc 1)`, `4,598,890,496 bytes`
- Source SHA-256: `c588a7dada3bf7175bfe97b238b0ab4c77df6401a58d766829aec9d92f3596e8`
- Patch: `Grandia3_KR_Disc1_v1.1.0_0a1ec442_full.xdelta`, `2,095,896,419 bytes`
- Patch SHA-256: `9507203e585145d703d2763bd14088f531c7dec92e68e00c4bd168f4c8b6bb51`
- Output SHA-256: `0a1ec442452b36f49e27794c5de475872ba9a9742f0a68a90c503deace104839`

→ [Open the v1.1.0 Release](https://github.com/Jungsik-won/Grandia3-KR-Translate-Disc-1/releases/tag/v1.1.0)

The release contains only an xdelta difference patch, hash-checking application scripts, documentation, and
checksums. It does not contain an original or patched ISO or extracted game assets. The installers
preserve the source ISO and verify the source, patch, and output hashes. Use only a legally owned
source dump.

<a id="japanese"></a>

## 🇯🇵 日本語

Grandia3-Translate は、PlayStation 2版『グランディアIII』日本版を対象とした非公式の韓国語化
プロジェクトです。内部開発版と公開テスト版 `v0.1.x-test` を経て、最初の正式版を `v1.0.0`
から開始します。

### 対応する元ISOと出力

- 元ISO: `Grandia III (Japan) (Disc 1)`、`4,598,890,496 bytes`
- 元ISO SHA-256: `c588a7dada3bf7175bfe97b238b0ab4c77df6401a58d766829aec9d92f3596e8`
- パッチ: `Grandia3_KR_Disc1_v1.1.0_0a1ec442_full.xdelta`、`2,095,896,419 bytes`
- パッチ SHA-256: `9507203e585145d703d2763bd14088f531c7dec92e68e00c4bd168f4c8b6bb51`
- 出力 SHA-256: `0a1ec442452b36f49e27794c5de475872ba9a9742f0a68a90c503deace104839`

→ [v1.1.0 Releaseを開く](https://github.com/Jungsik-won/Grandia3-KR-Translate-Disc-1/releases/tag/v1.1.0)

配布物にはxdelta差分パッチ、適用スクリプト、説明書、チェックサムのみが含まれます。元ISO、
パッチ済みISO、抽出したゲーム素材は含まれません。適用スクリプトは元ISOを保持し、元ISO・
パッチ・出力のハッシュを検証します。合法的に所有している元ISOにのみ適用してください。

<div align="center">

<sub>Grandia3-Translate · v1.1.0 · Korean fan translation research project</sub>

</div>
