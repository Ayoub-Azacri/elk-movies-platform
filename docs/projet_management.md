# Project Management

## Team

| Member | Role | Features |
|---|---|---|
| Ayoub Azacri| Developer | F2 raw ingestion, F5 DSL queries |
| Youssef El Hajji | Lead Tech | F1 ELK bootstrap, F8 search engine |
| Omar Hakik | Developer | F3 data cleaning, F4 explicit mapping |
| Youssef DEKHAIL | Developer | F6 Kibana dashboard, F7 documentation |

Youssef El Hajji owns the Docker Compose infrastructure and makes architectural decisions on mapping and indexing strategy. Other members own their features end-to-end: branch, implementation, PR, and merge.

## Feature status

| Feature | Description | Assignee | Status |
|---|---|---|---|
| F1 | Bootstrap ELK stack | Youssef El Hajji | Done — merged to `main` |
| F2 | Raw CSV ingestion (`movies_raw`) | Ayoub Azacri | Done — merged to `main` |
| F3 | Data cleaning pipeline (`movies_clean`) | Omar Hakik | Done |
| F4 | Explicit mapping + custom analyzer | Omar Hakik  | Done |
| F5 | 12 analytical DSL queries | Ayoub Azacri | Done |
| F6 | Kibana dashboard (6 visualizations) | Youssef DEKHAIL| Done |
| F7 | Documentation suite | Youssef DEKHAIL | In progress |
| F8 | Search engine (full-text + filters) | Youssef El Hajji | Not started |

## Timeline

| Date | Milestone |
|---|---|
| Early April 2026 | Project kickoff, planning poker session, branch strategy agreed |
| April 7–10 | F1 and F2 completed and merged |
| April 11–17 | F3, F4, F5, F6 in parallel |
| April 18–22 | F7 documentation, F8 search engine, final review |
| April 25, 2026 | Deadline — all deliverables submitted |

The deadline is firm. F8 is the highest-risk item still open as of April 21.

## Git workflow

This project uses GitFlow-lite: feature branches merge into `dev` (integration), then `dev` merges into `main` (stable).

Direct pushes to `main` or `dev` are not allowed.

### Branch naming

| Pattern | Purpose |
|---|---|
| `main` | Stable, releasable state. Never push directly. |
| `dev` | Integration branch. All PRs target this. |
| `feature/F<N>-<slug>` | Feature work, e.g. `feature/F2-ingestion-brute` |
| `fix/<slug>` | Bug fixes, e.g. `fix/logstash-date-parse` |

### Commit format

```
<type>(<scope>): <short description>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Scope is the feature number: `F1` through `F8`.

Examples:

```
feat(F2): add CSV ingestion pipeline with sincedb
fix(F3): handle null genres field in cleaning filter
docs(F5): add bool query examples to queries.md
```

Vague messages like `fix`, `update`, or `WIP` are not accepted.

### PR process

1. Branch from `dev`.
2. Open a PR targeting `dev`, not `main`.
3. At least 1 reviewer required before merge.
4. Each member must open at least 1 PR and review at least 1 PR.
5. Rebase on `dev` before opening the PR if the branch has diverged.
6. Never force-push `main` or `dev`.

### What not to commit

- `DATA/movies.csv` — too large, gitignored.
- `logs/sincedb_movies` — machine-specific state, gitignored.
- `.env` files or any credentials.

## Related files

[[planning_poker.md]] [[runbook.md]]