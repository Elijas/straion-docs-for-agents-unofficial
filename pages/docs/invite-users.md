---
title: "Invite Users"
source: https://straion.com/docs/invite-users
description: "How to invite team members to your Straion organization: add email addresses, manage pending invites, and assign member roles."
section: "Organization & Account"
order: 12
prev: validate-code.md
next: sso.md
---

# Invite Users

Bring your team into Straion so everyone shares the same set of rules and stays aligned. As an admin, you can invite people by email and manage their invites and roles from the **User Management** page.

This page covers inviting people manually. Straion also supports automatic provisioning through [**SCIM**](scim.md), which lets you sync users and roles from your identity provider.

## 1. Open Invite Users

From any page, click the **Invite Users** entry in the bottom-left navigation.

![The Rules page with the Invite Users navigation highlighted in the bottom-left sidebar](https://straion.com/.netlify/images?url=_astro%2F01-getting-started.nzrNzJDY.jpg&w=3248&h=2112&dpl=6a85597a97a15700076a9c5e)

## 2. Add email addresses

In the **Invite people** dialog, enter the email addresses of the people you want to invite. You can add several at once by separating them with commas, then click **Invite**.

![The &#x27;Invite people to demo&#x27; dialog with two comma-separated email addresses entered](https://straion.com/.netlify/images?url=_astro%2F02-invite-dialog.WIgNDhwQ.jpg&w=3824&h=2474&dpl=6a85597a97a15700076a9c5e)

## 3. Manage organization invites

Invited users appear under **Organization Invites** with a **Pending** status. Each invite is valid for 14 days. From the **Actions** column you can:

- **Resend Invite** — send the invitation email again, for example if it expired or was missed.
- **Copy invite link** — copy a direct link to your clipboard and share it with the invitee yourself.
- **Delete** — cancel a pending invite.

![The User Management page showing pending organization invites with Copy Invite Link and Resend Invite actions highlighted](https://straion.com/.netlify/images?url=_astro%2F03-pending-invites.Cc7HLmPl.jpg&w=3824&h=2474&dpl=6a85597a97a15700076a9c5e)

## Members and roles

Once an invite is accepted, the person moves into the **Organization Members** list, where you can manage their **Role** or **Deactivate** their access. Members provisioned through SCIM are flagged in the **Provisioned by SCIM** column.
