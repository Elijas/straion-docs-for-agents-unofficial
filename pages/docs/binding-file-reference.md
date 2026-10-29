---
title: "Binding file reference"
source: https://straion.com/docs/binding-file-reference
description: "The on-disk layout and file format for rule binding files in a central source."
section: "Rules"
order: 8
prev: rule-bindings.md
next: best-practices.md
---

# Binding file reference

A central source keeps its bindings as YAML files next to its rules. This page is the reference for that layout and file format: what a binding file looks like, what each field accepts, and the things you need to get right when you edit one by hand. To learn what bindings do and how to set them up, see [Rule bindings](rule-bindings.md).

## Layout

Binding files live on the `straion/rules/v1` branch, in a `bindings/` folder next to `rules/`. Each file is `<name>.yaml` or `<name>.yml`, directly in `bindings/`:

```plaintext
rules/
  idempotency/
    README.md
    ...
  payments-safety/
    README.md
    ...
  security/                   ← grouping folder
    payments/
      README.md
      ...
bindings/
  payments-safety.yaml        ← one binding
  secure-coding.yaml
```

Only a central source can have a `bindings/` folder. For the `rules/` folder, see [Rule file format](rule-file-format.md).

## Binding file

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: Payments safety rules for the services that move money.
collections:
  - idempotency
  - payments-safety
  - security/payments
repos:
  - github.com/acme/billing
  - github.com/acme/ledger
submodules: exclude
```

| Field | Required | Value |
| --- | --- | --- |
| `$schema` | Yes | `https://straion.com/schemas/rule-binding/v1.json` |
| `description` | Yes | Why these repositories get these rules. 10 to 300 characters. |
| `collections` | Yes | Folder paths of collections under `rules/` in the same source, for example `payments-safety` or `security/payments`. At least one. |
| `repos` | Yes | `all`, or a list of [repository keys](#repository-keys). At least one. |
| `submodules` | No | `exclude` (default) or `include`. With `include`, the collections also apply to repositories nested in a listed repository, at any depth. |

Other fields are errors.

## Repository keys

A repository key is the repository URL without the scheme, the user, and `.git`. For example, `https://github.com/acme/billing.git` and `git@github.com:acme/billing.git` both give `github.com/acme/billing`.

To find the key of a repository, run this command in it:

```bash
git remote get-url origin
```

Write the key in this form: the host in lowercase, no trailing `/`, and no wildcards. Keep a port only when it isn’t the default one, for example `git.acme.internal:8443/platform/billing`.

On `github.com`, `gitlab.com`, `bitbucket.org`, and `dev.azure.com`, the path is not case-sensitive. On other hosts it is.

## Things to get right

- **A collection is its folder path, not its `name`.** Use the path of the collection folder under `rules/`, grouping folders included: `security/payments`, not `payments`. See the [rules layout](rule-file-format.md#layout). Each folder in the path has lowercase letters, digits, and `-`, and starts with a letter or a digit. A binding can only list collections of its own source.
- **The folder is flat.** Put binding files directly in `bindings/`. A subfolder is an error. Files that start with `.` are ignored.
- **No YAML anchors or aliases.** Write each list out in full.
- **No central sources in `repos`.** A central source is never a target of a binding.

## How a file gets its collections

For each file that the agent edits, Straion finds the repository that owns the file. That is the repository of the nearest `.git` above the file. A git submodule is its own repository. A git worktree belongs to its main repository. A folder copied into a repository without its own `.git` (for example a subtree) belongs to the repository around it.

Straion takes the repository key from the `origin` remote. When there is no `origin`, it uses the only remote of the repository. With several remotes and none named `origin`, the repository has no usable remote.

The file gets a collection when one of these is true:

| Level | The collection comes from |
| --- | --- |
| `own` | The repository itself, when it is not a central source. |
| `direct` | A binding that lists the repository. |
| `inherited` | A binding with `submodules: include` that lists a repository that contains this one as a submodule, at any depth. |
| `all` | A binding with `repos: all`, a central collection that no binding lists, or a collection not from a repository. |

The levels only say why a collection applies. They don’t rank rules.

- Collections at level `own` don’t apply to the submodules of the repository.
- A parent repository doesn’t get the collections of its submodules.
- When the agent edits a file in the rules repository itself (a central source), no collections apply. Rule files and binding files aren’t checked against your rules.
- A file outside a git repository, or in a repository without a usable remote, gets only the `all` level. Straion prints a warning.
- When a parent repository has no usable remote, `submodules: include` bindings don’t reach its submodules. Straion prints a warning.
- When git can’t be read at all, the agent matches against every collection. Straion prints a warning.
- Each file is resolved alone. When the agent edits files in two repositories in one session, each file gets the collections of its own repository.
- The rules index at session start lists every collection. Only the rule search for a file applies bindings.
- Bindings take effect after the pull request is merged and `straion source repo sync` runs.

## Validate before you commit

To check your rules and bindings before you open a pull request, run this in a checkout of the rules branch:

```bash
straion source repo validate
```

It checks the files in `rules/` and `bindings/`, uncommitted edits included. It exits with a non-zero code and lists every error when something is invalid. It never changes files.

All problems are errors. A file with an error blocks the sync, and the sync rejects the whole commit. Each error names the file, and the field when there is one, for example `bindings/payments.yaml:repos.1`.

`validate` reports an error when:

- An entry in `bindings/` is a subfolder, or a file that isn’t `.yaml` or `.yml`.
- The file is not valid YAML, or uses an alias.
- `$schema` is missing or wrong.
- A field is unknown, has the wrong type, or has a value that is not permitted.
- `description` is shorter than 10 or longer than 300 characters.
- A `collections` entry is not a valid folder path, or is not a collection folder under `rules/` in this source.
- A `repos` entry is not a repository key in the form above.
- A `repos` entry is a central source.
- The source has a `bindings/` folder but is not central. An organization admin can run `straion source repo connect --central`.

## Commands

| Command | What it does |
| --- | --- |
| `straion source repo connect --central` | Makes the current repository a central source. Organization admins only. It writes no files. |
| `straion source repo connect --no-central` | Makes the current repository a normal source again. Organization admins only. It writes no files. |
| `straion source repo validate [--remote <name>]` | Validates `rules/` and `bindings/`. `--remote` defaults to `origin`. |
| `straion source repo sync [--dry-run] [--remote <name>]` | Validates and uploads rules and bindings. Run it in CI after each merge. `--dry-run` validates without uploading. |

Inside a checkout that has `rules/` or `bindings/` at its root, `validate` reads that working tree. Elsewhere it reads the `straion/rules/v1` branch of the repository. It always checks that the source is central and that no binding lists a central source.

## Stop using a central source

Run `straion source repo connect --no-central` in a checkout of the repository. Its collections then apply only to the repository itself again.

Straion keeps the binding files but ignores them. The next sync of a source that still has a `bindings/` folder fails, because only a central source can have bindings. Remove the `bindings/` folder with a pull request.
