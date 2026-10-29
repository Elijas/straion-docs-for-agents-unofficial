---
title: "Rule bindings"
source: https://straion.com/docs/rule-bindings
description: "Apply rule collections from one repository to other repositories, and review each change through a pull request."
section: "Rules"
order: 7
prev: rule-file-format.md
next: binding-file-reference.md
---

# Rule bindings

By default, the rules of a [connected repository](connect-repository.md) apply only to that repository. Rule bindings let you apply them to other repositories too.

A binding is a small YAML file in your rules repository. It says: these collections apply to these repositories.

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: Payments safety rules for the services that move money.
collections:
  - payments-safety
repos:
  - github.com/acme/billing
  - github.com/acme/ledger
submodules: exclude
```

You change bindings through pull requests, like the rules themselves. A binding applies after its pull request is merged and the source is synced.

## Examples

Each example is one file in the `bindings/` folder of your rules repository. To set up that repository the first time, see [Set up bindings](#set-up-bindings). For every field and check, see [Binding file reference](binding-file-reference.md).

### Apply collections to every repository

Set `repos` to `all`.

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: Baseline rules that every repository in the organization must obey.
collections:
  - secure-coding
  - logging
repos: all
submodules: exclude
```

**Result:** your agents follow `secure-coding` and `logging` in every repository.

### Apply collections to a team’s repositories

List each repository by its key, for example `github.com/acme/billing`. See [Repository keys](binding-file-reference.md#repository-keys).

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: Payments safety rules for the services that move money.
collections:
  - idempotency
  - payments-safety
repos:
  - github.com/acme/billing
  - github.com/acme/ledger
submodules: exclude
```

**Result:** your agents follow both collections in `billing` and `ledger`, and nowhere else. To add a repository later, add its key to the list.

### Apply collections to a repository and its submodules

Set `submodules` to `include`.

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: Embedded C rules for the firmware and all the libraries it vendors.
collections:
  - embedded-c
repos:
  - github.com/acme/firmware
submodules: include
```

**Result:** your agents follow `embedded-c` in `firmware` and in every submodule of `firmware`, however deep.

### Roll out a new collection step by step

Start with one pilot repository:

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: New API design rules, tried first on the billing service.
collections:
  - api-design
repos:
  - github.com/acme/billing
submodules: exclude
```

When the pilot goes well, add more repositories to `repos`. When the rules are ready for everyone, change `repos` to `all`. Each step is one pull request, so the team reviews each widening.

**Result:** the rules reach more repositories only when a reviewer approves it.

### Combine an organization baseline with team rules

The platform team binds a baseline to `all`, as in [the first example](#apply-collections-to-every-repository). Each team has its own rules repository, for example `acme/payments-rules`, and binds its collections to its own repositories:

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: Payments team rules for the payments services.
collections:
  - payments-logging
repos:
  - github.com/acme/billing
  - github.com/acme/ledger
submodules: exclude
```

**Result:** in `billing`, your agents follow the payments rules and the baseline. Each team changes its own rules without waiting for the platform team.

## Set up bindings

You do this once for each rules repository. It is a normal connected repository that you mark as central.

1. **Connect the rules repository.** Follow [Connect a repository](connect-repository.md). You can use a new repository or one that is already connected.
2. **Mark it as central.** Run this command in a checkout of the repository. You must be an organization admin.

   ```bash
   straion source repo connect --central
   ```

   It adds no files. You add them in the next steps.
3. **Check that CI syncs the rules branch.** Use the two workflows from [Connect a repository](connect-repository.md#step-3-sync-on-every-change): `straion source repo sync` after each merge, and `straion source repo sync --dry-run` on each pull request. They check and upload the bindings together with the rules, so bindings need no extra job. Mark the pull request check as required in your branch protection, so an invalid binding can’t be merged.
4. **Protect the branch.** Require a review for `straion/rules/v1`, and do not push to it directly. To choose who must approve, add a `CODEOWNERS` file on the branch:

   ```plaintext
   /bindings/ @acme/platform
   /rules/ @acme/platform
   /rules/payments-safety/ @acme/payments
   ```

   The last matching line wins. Here the payments team approves changes to the `payments-safety` collection, and the platform team approves all other changes. `CODEOWNERS` blocks a merge only when the branch protection has **Require review from Code Owners** turned on. On GitLab and Bitbucket, use their code owners feature and the matching approval rule.
5. **Add your first binding.** Pick an [example](#examples), save it as `bindings/<name>.yaml` on a work branch, and open a pull request into `straion/rules/v1`.

## Change a binding

A change to a binding changes which rules your agents follow. Review it like code:

1. Edit `bindings/*.yaml` on a work branch. Run `straion source repo validate` to check the files.
2. Open a pull request against `straion/rules/v1`. Give the reason for the change in the description.
3. CI validates the bindings. A reviewer approves.
4. After the merge, CI runs `straion source repo sync`. The new bindings apply from that point.

Common changes:

- **Onboard a new repository.** Add its key to `repos` in each binding that it needs.
- **Remove a collection from a repository.** Remove the collection from `collections`, or the repository from `repos`.

## Which rules your agent follows

When your agent works on a file, it follows the collections that apply to the repository of that file. Things that surprise people:

- **Own rules stay in their repository.** A submodule doesn’t get the rules of the repository around it. Use `submodules: include` to send rules down.
- **A parent repository doesn’t get the rules of its submodules.**
- **Bindings work on whole repositories.** You can’t bind a collection to one folder.
- **Your agent gets no rules in the rules repository itself.** Editing rules and bindings isn’t checked against them.
- **Without a remote, your agent gets only the rules for every repository.** This happens outside a git repository, or in a repository without a usable remote. Straion prints a warning.
- **A fork is its own repository.** Straion uses the `origin` remote, which in a fork is usually your fork. Bindings for the upstream repository don’t reach it.
- **Your agent still sees every collection name at the start of a session.** The rules it checks a file against are only the ones that apply.

For the exact resolution, see [How a file gets its collections](binding-file-reference.md#how-a-file-gets-its-collections).
