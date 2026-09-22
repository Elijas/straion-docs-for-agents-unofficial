---
title: "Troubleshooting"
source: https://straion.com/docs/troubleshooting
description: "Solutions to common Straion issues: agent setup checks, firewall and permission problems, skills that do not show up after setup, and SAML SSO and SCIM provisioning errors."
section: "References"
order: 16
prev: cli-api-reference.md
---

# Troubleshooting

Running into a problem? This page covers the most common issues users encounter with Straion. Jump to the relevant section:

## Prerequisites

- Access to one or more of these coding agents: Claude Code (minimum version 2.1.84), Cursor, or GitHub Copilot
- A Straion account
- MacOS/Windows and Node.js v22+
- Sufficient permissions on your computer to install the Straion CLI

## Check Agent Setup

Before connecting Straion, verify your coding agent CLI is installed. Run the command for your agent:

| Agent | Check command | Supported version |
| --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/setup) | `claude --version` | > 2.1.84 |
| [GitHub Copilot](https://docs.github.com/copilot/how-tos/set-up/install-copilot-cli) | `copilot --version` | > 1.0.0 |
| [Cursor](https://cursor.com/docs/cli/installation) | `agent --version` | > 3.0.0 |

If a command is not found, follow the install guide linked in the table above.

## Firewall Issues

Some corporate or network firewalls may block outbound requests from the Straion CLI. If you’re seeing connection errors or timeouts, check with your network administrator to ensure that outbound HTTPS traffic to Straion’s services is allowed.

## Permission Issues

Double-check your user token or generate a new one in the [User Settings](http://straion.app/auth/login?redirectUrl=%2Fsettings%2Fuser-tokens). The token inherits your permissions and can be scoped with an expiration date.

## Common issues

### Agent setup finished, but skills are not available

First, upgrade your agent to a supported version (see the table above) and run `straion setup` again.

If the skills are still missing in Claude Code, check for a name collision. Straion installs its skills into `~/.claude/skills`, the directory Claude Code scans for user-level skills:

```text
~/.claude/skills/
├── straion-import-rules
├── straion-check-compliance
└── straion-implement
```

Setup skips any name that is already taken, so an unrelated skill called `straion-implement` silently blocks ours. Rename or remove the conflicting directory and run `straion setup` again.

A skill in your repository shadows a user-level skill of the same name. If `.claude/skills/` in the project defines one of the names above, the project copy wins. Rename it, or remove it if it was a leftover.

### The agent lists a skill twice, or under an old name

Straion skills used to live inside the plugin directory, where Claude Code loaded them under a `straion:` prefix. They now live in `~/.claude/skills` and carry a `straion-` prefix in the name itself:

| Old | New |
| --- | --- |
| `/straion:import-rules` | `/straion-import-rules` |
| `/validating-rules` | `/straion-check-compliance` |
| `/developing-with-rules` | `/straion-implement` |

Run `straion setup` to pick up the new set. Setup also deletes the copies an earlier install left inside the plugin, which is what caused the duplicates. The plugin itself stays: it still provides Straion’s hooks.

Start a fresh agent session afterwards, since skills are loaded at session start.

## SAML SSO

Setup steps live on the [SAML SSO](sso.md) page.

### ”The connection is not setup for login. Please contact your organization admin!”

No SAML connection exists for that subdomain. Check the spelling (the subdomain is the slug in your workspace URL — `acme` for `acme.straion.app`) and confirm the connection exists on the Identity & provisioning page.

### ”User not part of organization”

SSO authenticated the user, but they aren’t a member of your Straion organization yet. [Invite them](invite-users.md) or provision them via [SCIM](scim.md) first. The email address in your IdP must match their Straion account email exactly.

### ”SAML connection could not be created / updated”

Straion couldn’t fetch or parse the metadata. Two common causes:

- The **metadata URL** isn’t reachable from Straion’s servers (e.g. it requires an authenticated session). Download the XML and paste it instead — and clear the Metadata URL field, since a filled URL takes precedence over pasted XML.
- The **pasted XML is incomplete or was reformatted** by an editor. Re-download the metadata from your IdP and paste it unmodified.

### Login loops back to the login page

The assertion was rejected. Verify the **Audience URI** in your IdP exactly matches the value shown in Straion (including the scheme, no trailing slash) and that the NameID is the user’s email address.

## SCIM provisioning

Setup steps live on the [SCIM provisioning](scim.md) page.

### The IdP’s connection test fails with 401 Unauthorized

The bearer token doesn’t match. Copy the **SCIM Secret** again (use the copy button — a revealed secret can be mis-selected) and make sure the authentication mode is *HTTP Header / Bearer token*. If the connection was deleted and recreated in Straion, the old secret is no longer valid.

### ”User already exists” when assigning someone

The user was already provisioned through this connection — usually after retrying a partially failed assignment. Unassign and re-assign them, or check whether they already appear in User Management.

### A provisioned user can’t log in with SSO

SCIM and SSO match users by **email address**. Make sure the email your IdP sends via SCIM is the same one used as the SAML NameID (see [SAML SSO](sso.md)).

### Deprovisioned users still appear in User Management

They’re deactivated, not deleted — access is already revoked. The default member list hides them; enable the *show deactivated* toggle to see them.

### Groups from my IdP aren’t showing up in Straion

Straion doesn’t sync groups yet. Assigning a group in your IdP provisions its members as individual users — the members get access, but the group itself isn’t created in Straion.

## More Coming Soon

Troubleshooting content is on its way. If you’re running into an issue, reach out to support via email at [support@straion.com](mailto:support@straion.com) or on [Discord](https://discord.gg/KjgK5EHP74) and we’ll help you get unblocked.
