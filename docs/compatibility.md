# 도구별 설치와 사용

`adaptive-testing`의 공통 부분은 `SKILL.md`와 `references/`다. 도구 전용 API, 모델 이름, 실행 권한 설정, 동적 명령 치환을 사용하지 않는다. 같은 규칙을 호스트의 파일·터미널·테스트 도구로 수행한다.

`agents/openai.yaml`은 Codex의 표시 정보다. 다른 도구에 없어도 공통 규칙을 사용할 수 있다. 이 문서와 설치 도구는 로컬 개발 환경을 대상으로 한다.

## 지원 경로

아래 경로 뒤에 `adaptive-testing/`이 붙는다. `~`는 각 운영체제의 사용자 홈 폴더다. 공식 문서 확인일: **2026-10-06**.

| 설치 도구의 `--tool` | 프로젝트 스킬 루트 | 개인 스킬 루트 | 공식 근거 |
| --- | --- | --- | --- |
| `codex` | `.agents/skills/` | `~/.agents/skills/` | [Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) |
| `claude-code` | `.claude/skills/` | `~/.claude/skills/` | [Claude Code](https://code.claude.com/docs/en/skills#choose-where-skills-load) |
| `antigravity` | `.agents/skills/` | `~/.gemini/config/skills/` | [Antigravity 2.0 / IDE](https://www.antigravity.google/docs/skills) |
| `antigravity-cli` | `.agents/skills/` | `~/.gemini/antigravity-cli/skills/` | [Antigravity CLI](https://www.antigravity.google/docs/skills#cli-skill-locations) |
| `cursor` | `.cursor/skills/` | `~/.cursor/skills/` | [Cursor](https://cursor.com/docs/skills#skill-directories) |
| `generic` | `--skills-dir`로 지정 | `--skills-dir`로 지정 | 사용하는 호스트의 실제 스킬 경로 확인 |

Antigravity는 현재 `.agents/skills`를 기본으로 사용한다. 기존 `.agent/skills`와 IDE의 `~/.gemini/antigravity/skills`는 호환 경로다. CLI와 IDE의 개인 경로를 혼동하지 않는다. [공식 안내](https://www.antigravity.google/docs/skills)

Cursor는 `.agents/skills`도 읽는다. 여러 도구가 같은 프로젝트를 사용하면 공통 폴더를 재사용할 수 있다. 설치 도구의 `cursor` 기본값은 도구를 명시한 `.cursor/skills`다. [공식 안내](https://cursor.com/docs/skills#skill-directories)

## 설치 선택

저장소 루트에서 실행한다. Python 3.9 이상과 표준 라이브러리만 필요하며, 스킬을 사용하는 동안에는 Python 설치 도구를 실행하지 않는다.

```sh
# 프로젝트에 설치: 경로는 실제 작업 프로젝트로 변경
python scripts/install.py --tool claude-code --project ../my-project

# 개인 환경에 설치
python scripts/install.py --tool antigravity --user

# 설치 예정 위치만 확인: 파일이나 폴더를 만들지 않음
python scripts/install.py --tool cursor --project ../my-project --dry-run

# 다른 Agent Skills 호스트: 스킬 루트를 직접 지정
python scripts/install.py --tool generic --skills-dir ../my-project/custom-skills
```

`--project`, `--user`, `--skills-dir` 중 하나만 선택한다. `--skills-dir`은 **스킬들의 상위 폴더**이며, 그 안에 `adaptive-testing`을 만든다. `generic`은 호스트 경로를 추측하지 않으므로 `--skills-dir`이 필수다.

기존 설치가 같은 공통 규칙을 포함하면 재실행은 변경 없이 끝난다. 로컬에서 달라진 규칙이나 불완전한 설치가 있으면 중단한다. 기존 사용자 파일을 덮어쓰거나 삭제하는 강제 옵션은 제공하지 않는다.

### 기존 Codex 개인 경로 사용

이 저장소의 이전 안내로 `~/.codex/skills` 또는 `$CODEX_HOME/skills`에 설치했다면, 새 위치에 중복 설치하지 말고 기존 폴더를 계속 관리한다. 설치 도구가 사용자 설정을 탐색하거나 옮기지는 않는다.

```sh
python scripts/install.py --tool codex --skills-dir ~/.codex/skills --dry-run
```

사용자 지정 `$CODEX_HOME`을 쓰는 경우 해당 경로의 `skills` 폴더를 직접 지정한다. PowerShell 예:

```powershell
python scripts/install.py --tool codex --skills-dir (Join-Path $env:CODEX_HOME 'skills') --dry-run
```

### Python 없이 복사

`skills/adaptive-testing` 폴더를 위 표의 스킬 루트 아래에 복사하면 된다. 다음은 기존 설치가 없는 Claude Code 프로젝트에 복사하는 예다.

```sh
mkdir -p ../my-project/.claude/skills
cp -R skills/adaptive-testing ../my-project/.claude/skills/
```

```powershell
New-Item -ItemType Directory -Force '../my-project/.claude/skills' | Out-Null
Copy-Item -LiteralPath './skills/adaptive-testing' -Destination '../my-project/.claude/skills' -Recurse
```

수동 복사 시 포함되는 `agents/openai.yaml`은 Codex용이며, 다른 도구에서는 참조할 필요가 없다. 반드시 `references/selective-validation.md`까지 함께 복사한다.

## 호출 방법

| 도구 | 명시적으로 사용하는 방법 |
| --- | --- |
| Codex | `$adaptive-testing 이번 변경을 검증해줘.` |
| Claude Code | `/adaptive-testing 이번 변경을 검증해줘.` |
| Antigravity 2.0 / IDE | `adaptive-testing 스킬을 사용해 이번 변경을 검증해줘.` |
| Antigravity CLI | `/adaptive-testing 이번 변경을 검증해줘.` |
| Cursor | Agent 채팅에서 `/` 입력 → `adaptive-testing` 검색·선택 → 검증 요청 |

호출법 근거: [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills), [Antigravity](https://www.antigravity.google/docs/skills), [Cursor](https://cursor.com/docs/skills).

공통으로 이름과 설명에 따른 자동 선택을 사용할 수 있지만, 설치만으로 모든 작업에 강제 적용되는 것은 아니다. 처음에는 명시적으로 호출해 선택되는지 확인한다. 조직 정책, 도구 버전, 세션 범위에 따라 로딩 가능 여부가 달라질 수 있다.

## 스킬 기능이 없는 도구

공통 폴더를 프로젝트의 읽을 수 있는 위치에 두고 파일을 직접 읽도록 요청한다. 예를 들어 이 저장소를 열었다면:

```text
skills/adaptive-testing/SKILL.md를 읽고 이번 변경 검증에 적용해줘.
상세 규칙은 해당 파일에서 필요하다고 안내하는 경우에만 읽어줘.
```

이 경우 스킬 자동 검색이나 슬래시 명령 지원을 전제로 하지 않는다. 파일을 읽을 수 없는 호스트라면 본문을 컨텍스트로 제공해야 하며, 지연 로딩의 장점은 줄어든다. 도구별 전역 지침 파일에 전체 본문을 중복해서 넣기보다 공통 파일의 위치와 적용 시점을 짧게 연결한다.

## 확인 범위

이 저장소의 자동 검사는 임시 디렉터리에서 도구별 경로, 공통 파일 복사, Codex 메타데이터 분리, 재설치, 충돌 시 파일 보존, dry run을 확인한다. 실제 Claude Code·Antigravity·Cursor 앱 세션의 동작 검증과는 구분한다.

각 도구에서 처음 사용할 때는 스킬 목록이나 명시적 호출로 로딩을 확인하고, 필요한 작은 변경을 검증하면서 실행 범위가 지침과 맞는지 확인한다. 미실행·실패한 검사는 통과로 보고하지 않는다.

[README로 돌아가기](../README.md)
