# test.zip

**test.zip — Run less. Catch more.**

코딩 에이전트가 변경에 필요한 검증을 고르고, 같은 검사를 불필요하게 반복하지 않도록 돕는 **테스트 운영 스킬**이다. 작은 프로젝트는 전체 빠른 검사를 그대로 실행하고, 선택 실행의 이득이 확인될 때만 구조를 확장한다.

**Codex · Claude Code · Antigravity · Cursor**에서 같은 규칙을 사용한다. 도구별로 달라지는 것은 설치 경로와 호출 방법이다.

<picture>
  <source media="(max-width: 600px)" srcset="docs/overview-mobile.svg">
  <img src="docs/overview.svg" alt="adaptive-testing 구조: 기본 규칙을 읽고 Simple, Light, Selective 후보 중 하나를 정한다. 위험에 따른 검증은 항상 추가하며, 복잡한 영향 분석은 필요할 때만 상세 문서를 읽는다.">
</picture>

> **그림을 텍스트로 읽으면:** `SKILL.md`가 기본 규칙을 제공한다. 전체 빠른 검사가 짧으면 그대로 실행한다. 길어지면 기존 필터를 활용하고, 반복 비용이 커지면 선택 실행의 이득을 계산한다. 변경 위험에 필요한 검증은 모든 모드에 적용한다. 결과 재사용은 검증 입력이 일치할 때만 허용한다.

[시작하기](#시작하기) · [도구별 호환성](docs/compatibility.md) · [파일 구조](#파일-구조) · [전환 기준](#전환-기준) · [실행 흐름](#실행-흐름)

## 시작하기

이 저장소에는 테스트 실행기나 자동 영향 분석 엔진이 없다. `adaptive-testing`은 에이전트가 기존 프로젝트의 명령과 테스트를 활용할 때 따르는 지침이다. 설치만으로 Git hook이나 CI 설정이 바뀌지는 않는다.

먼저 저장소를 받는다. 스킬 자체에는 런타임 의존성이 없으며, 아래의 선택적 설치 도구만 Python 3.9 이상을 사용한다. 추가 패키지는 필요 없다.

```sh
git clone https://github.com/kcc920926-droid/test.zip.git
cd test.zip
```

사용할 도구를 골라 **실제 작업 프로젝트**에 설치한다. `../my-project`는 이미 존재하는 프로젝트 경로로 바꾼다. 다음 명령 중 필요한 것만 실행하면 된다.

```sh
python scripts/install.py --tool claude-code --project ../my-project
python scripts/install.py --tool antigravity --project ../my-project
python scripts/install.py --tool codex --project ../my-project
python scripts/install.py --tool cursor --project ../my-project
```

Windows에서도 같은 명령을 사용한다. 환경에 따라 `python`을 `py -3` 또는 `python3`로 바꾼다. 경로에 공백이 있으면 따옴표로 감싼다.

| 도구 | 프로젝트에 생성되는 경로 | 호출 예 |
| --- | --- | --- |
| Codex | `.agents/skills/adaptive-testing/` | `$adaptive-testing 이번 변경을 검증해줘.` |
| Claude Code | `.claude/skills/adaptive-testing/` | `/adaptive-testing 이번 변경을 검증해줘.` |
| Antigravity 2.0 / IDE | `.agents/skills/adaptive-testing/` | `adaptive-testing 스킬로 이번 변경을 검증해줘.` |
| Antigravity CLI | `.agents/skills/adaptive-testing/` | `/adaptive-testing 이번 변경을 검증해줘.` |
| Cursor | `.cursor/skills/adaptive-testing/` | Agent 채팅에서 `/` 입력 후 `adaptive-testing` 선택 |

프로젝트 수준의 Codex와 Antigravity는 같은 `.agents/skills` 폴더를 공유하므로 한 번만 설치해도 된다. 도구별 공식 경로·호출법과 버전 차이는 [호환성 안내](docs/compatibility.md)에 정리했다.

프로젝트에 쓰기 전에 설치 위치와 파일만 확인하려면 `--dry-run`, 현재 사용자 전체에 설치하려면 `--user`를 사용한다.

```sh
python scripts/install.py --tool claude-code --project ../my-project --dry-run
python scripts/install.py --tool claude-code --user
python scripts/install.py --tool antigravity --user
python scripts/install.py --tool antigravity-cli --user
```

설치 도구는 기존 공통 규칙이 같으면 아무것도 바꾸지 않고, 내용이 다르거나 불완전하면 덮어쓰지 않고 종료한다. 기존 버전 업데이트는 변경 내용을 비교한 뒤 수동으로 반영한다. `CLAUDE.md`, `GEMINI.md`, hook, CI 설정은 수정하지 않는다.

Python 없이 폴더를 복사하는 방법, 기존 Codex 경로, 다른 Agent Skills 도구, 스킬 기능이 없는 도구에서의 사용법도 [호환성 안내](docs/compatibility.md)에 있다.

## 파일 구조

```text
test.zip/
├── README.md                          사람이 읽는 구조와 사용법
├── docs/
│   ├── compatibility.md              도구별 설치·호출·확인 방법
│   ├── overview.svg                   데스크톱용 설명 그림
│   └── overview-mobile.svg            모바일용 설명 그림
├── scripts/
│   └── install.py                     선택한 도구의 경로로 스킬 복사
├── tests/
│   └── test_install.py                경로·충돌·파일 보존 검사
└── skills/
    └── adaptive-testing/
        ├── SKILL.md                   기본 판단과 실행 규칙
        ├── agents/
        │   └── openai.yaml            Codex 전용 표시 정보 · 선택 사항
        └── references/
            └── selective-validation.md  선택 실행의 상세 기준
```

| 파일 | 역할 | 읽는 시점 |
| --- | --- | --- |
| [SKILL.md](skills/adaptive-testing/SKILL.md) | 모드 선택, 위험별 검증, 중복 실행 방지 | 스킬 적용 시 |
| [selective-validation.md](skills/adaptive-testing/references/selective-validation.md) | 비용 계산, 영향 범위, 캐시·CI 적용 조건 | 선택 실행을 검토하거나 불확실성을 해소할 때 |
| [openai.yaml](skills/adaptive-testing/agents/openai.yaml) | Codex 전용 표시 이름과 설명. 공통 실행에 필요하지 않음 | Codex가 스킬 정보를 표시할 때 |
| [install.py](scripts/install.py) | 같은 원본을 도구별 검색 경로에 복사. Codex 신규 설치에만 UI 메타데이터 추가 | 설치할 때만 실행 |

상세 문서는 필요할 때만 읽는다. 작은 변경마다 영향 분석 체계를 설계하거나 긴 검사 계획을 작성하지 않도록 구성했다.

스킬 본문을 도구별로 복제·수정하지 않는다. 공통 `SKILL.md`와 `references/`가 판단 규칙의 원본이고, 도구별 설치 정보는 README와 호환성 문서에서 관리한다.

## 전환 기준

기준은 **테스트 개수가 아니라 피드백을 얻는 실제 비용**이다. 아래 시간은 조정 가능한 초기값이며, 업계 표준이나 강제 제한 시간이 아니다.

| 전체 빠른 검사 시간 | 모드 | 에이전트의 행동 |
| --- | --- | --- |
| 미측정 또는 30초 이내 | **Simple** | 기존 빠른 검사를 전체 실행한다. 영향 지도나 점수 체계를 만들지 않는다. |
| 30초 초과~90초 | **Light** | 기존 패키지·파일 필터가 분명히 이득일 때만 사용한다. 새 분석 도구는 도입하지 않는다. |
| 90초를 반복해서 초과 | **Selective 후보** | 선택 실행의 절약 시간이 판단·구축·유지 비용보다 큰지 확인한다. |

**빠른 검사**는 lint, typecheck, unit과 이미 묶여 있는 저비용 contract 검사다. Full E2E와 전체 브라우저 조합은 포함하지 않는다. 문서만 바뀌었다면 해당 문서에 필요한 검사만 수행한다.

가능하면 평소 실행 약 5회의 중앙값을 참고하고, 최초 실행과 준비된 환경의 실행을 구분한다. 측정만을 위한 반복 실행은 하지 않는다. 모드는 작업 단위로 정하며, 기존에 효과적인 선택 실행이 있다면 시간대가 조금 바뀌었다는 이유만으로 매번 전환하지 않는다.

### 선택 실행이 정말 이득인 경우

```text
1회 절약 시간 = 전체 검사 시간 - 선택 검사 시간 - 선택 판단 시간

기간 내 순이득 = 반복 횟수 × 1회 절약 시간
               - 초기 구축 비용 - 유지 비용
```

모든 비용은 비교 가능한 시간 단위로 계산한다. 판단 시간에는 에이전트의 추론과 도구 호출이 포함된다. 다음은 실제 벤치마크가 아닌 설명용 예시다.

| 전체 검사 | 선택 검사 | 판단 비용 | 해석 |
| ---: | ---: | ---: | --- |
| 18초 | 7초 | 12초 | 선택 실행이 1초 느리다. **전체 실행 유지.** |
| 60초 | 18초 | 2초 | 기존 필터로 40초 절약. **가벼운 필터 활용.** |
| 180초 | 30초 | 5초 | 1회 145초 절약. 하루 10회면 약 24분이며, 구축·유지 비용을 추가로 비교한다. |

전체 120초 중 서버 초기화가 대부분이고 선택 실행도 110초라면, 먼저 초기화·빌드·데이터 준비 비용을 살펴본다. 느리다는 사실만으로 영향 분석 도입이 정당화되지는 않는다.

## 실행 흐름

| 시점 | 실행 원칙 |
| --- | --- |
| 구현 중 | 파일마다 실행하지 않고 하나의 동작 변경을 완성한 뒤 검증한다. 버그는 최소 재현 테스트부터 확인한다. |
| commit 전 | staged 내용에 맞는 검사 결과를 확인한다. 검증 입력이 같은 유효한 성공 결과는 재사용할 수 있다. |
| push 전 | 필요한 integration·smoke를 조건부 실행한다. 프로젝트의 필수 hook은 따른다. |
| PR / merge | 요구되는 CI 검증을 해당 코드 상태에서 완료한다. 로컬 통과로 필수 CI를 대체하지 않는다. |
| nightly | 더 넓은 회귀·브라우저 조합과 선택 누락을 점검한다. 병합 전 필수 검증은 미루지 않는다. |

실패하면 **실패한 테스트 재현 → 원인 확인 → 수정 → 재현 테스트 확인 → 수정 영향 범위 재검증** 순서로 진행한다. 이전에 실패한 테스트만 통과했다고 나머지 검사까지 완료된 것으로 보지 않는다.

## 지켜야 할 검증

**실행 모드는 비용을 조절한다. 필요한 검증 범위는 변경 위험으로 결정한다.**

| 변경 | 추가로 확인할 범위 |
| --- | --- |
| 내부 계산·변환 로직 | 관련 unit, 패키지 단위 typecheck와 필요한 소비 모듈 |
| UI 동작·라우팅 | component 검사, 브라우저·계층 간 동작에 필요한 관련 E2E |
| API·서비스 경계 | contract·integration, 영향을 받는 사용자 흐름 |
| 인증·권한·결제·migration·공통 기반 | 도메인 필수 검사와 필요한 E2E를 병합 전에 완료 |

선택 실행에는 직접 변경한 테스트, 변경 모듈을 사용하는 모듈의 테스트, API·DB 같은 경계의 명시적 매핑, 위험별 필수 검사를 합친다. 코드가 바뀌었는데 테스트가 0개 선택되거나 영향 범위가 불명확하면 패키지·도메인 단위로 범위를 넓힌다.

결과를 재사용하려면 소스, 의존 모듈, 테스트, 설정, 의존성 버전, 관련 환경, 실제 검증한 코드 상태가 일치해야 한다. 공유 서버나 외부 상태에 의존하는 E2E 결과는 기본적으로 캐시하지 않는다.

- Full E2E는 기본적으로 CI에서 실행한다. 명시적 요청이나 프로젝트의 필수 규칙은 따른다.
- 시간 목표를 넘겼다고 남은 검사를 생략하거나 통과로 처리하지 않는다.
- 재시도 성공만으로 테스트를 격리하거나 assertion을 약화하지 않는다.
- 선택 실행 도입 초기에는 넓은 CI 검증을 유지하고 누락 여부를 비교한다.

## 설명의 근거

설치 도구의 회귀 검사는 다음 명령으로 실행한다. 임시 폴더를 사용하며 실제 사용자 스킬 폴더에는 쓰지 않는다.

```sh
python -m unittest discover -s tests -v
```

검증 범위는 설치 경로·파일 내용·기존 파일 보존·문서 및 SVG 형식이다. Claude Code, Antigravity, Cursor의 실제 앱 세션에서 자동 선택과 테스트 실행까지 검증한 것은 아니다.

이 README와 그림은 저장소에 포함된 [기본 규칙](skills/adaptive-testing/SKILL.md)과 [상세 기준](skills/adaptive-testing/references/selective-validation.md)을 설명한다. 특정 프로젝트의 성능 개선을 측정한 결과는 아니다.

시각 설명은 [explain_me](https://github.com/kcc920926-droid/explain_me)의 지침에 따라 작성했다. SVG는 외부 스크립트·폰트 서비스 없이 표시되며, 모바일 구성과 밝은/어두운 테마를 포함한다.
