---
name: home-assistant-agent-operations
skill_type: skill
description: >-
  Operate home-assistant-agent through its governed MCP and Arbora capabilities, including home assistant entity control, home assistant scene automation, home assistant telemetry history. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
---

# Home Assistant Agent Operations

Use the provider's governed MCP tools through Arbora delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current per-operation tool surface; never assume a stale tool name or schema.
3. Prefer read-only inspection first. For changes, present impact and use the provider's
   dry-run or preview mode when available.
4. Execute mutations as fenced WorkItems so retries remain idempotent and auditable.
5. Ingest source data only through the signed connector preset and ChangeEnvelope path.
6. Verify the durable result and its trace/evidence before reporting completion.

## Steps

1. Confirm the instance answers with `home_assistant_status` and verify the reply reports it as running.
2. Find the matching workflow by reading `references/catalog.md` and verify the workflow you plan to follow is listed there.
3. Run the read-only tool first, for example `home_assistant_get_state`(entity_id), and verify the result matches the request.
4. Preview the supported change with `home_assistant_get_services_for_target`(target) and get the requester's approval before any mutation, and verify the approval names the target.
5. Read the same object back with `home_assistant_get_state`(entity_id) and verify the durable result before reporting completion.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| Calls answer 401 or 403 | `HOME_ASSISTANT_TOKEN` is missing, expired or revoked | Create a new long-lived access token in the Home Assistant profile page, set `HOME_ASSISTANT_TOKEN`, and confirm with `home_assistant_status` |
| Calls time out or the connection is refused | `HOME_ASSISTANT_URL` is wrong or the instance is down | Correct `HOME_ASSISTANT_URL` including the port and scheme, then confirm with `home_assistant_ping` |
| A tool name or schema is not recognized | The surface changed since it was last read | Re-read `references/catalog.md`, open the linked workflow for the skill that covers the request, and use the tool names and parameters it lists |

## Safety contract

- Never persist credentials, endpoints, raw personal identifiers, hostnames, or local paths.
- Resolve TLS trust and verification from environment/configuration; never hardcode bypasses.
- Treat unknown ACL, tenant, schema, or tool-contract state as a hard failure.
- Require explicit approval for destructive, externally visible, or irreversible actions.
- Keep runtime traces policy-scoped and privacy-sanitized.

## Specialized workflows

Read [the workflow catalog](references/catalog.md) only when the request needs a
provider-specific procedure, parameter map, script, or reference asset.
