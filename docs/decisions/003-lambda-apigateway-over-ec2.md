# ADR-003: Use Lambda + API Gateway over an EC2-Hosted Backend

- **Status:** Accepted
- **Date:** 2026-04-19
- **Deciders:** Jeian Jasper

## Context

The visitor counter needs a single HTTP endpoint that increments a
DynamoDB item and returns the new count. Traffic pattern: spiky, low
baseline, near-zero when idle. Uptime cost must remain $0 for a
portfolio site.

## Decision

Expose an **HTTP API (API Gateway v2)** fronting a **Python Lambda
function** that uses `boto3` to update the DynamoDB item.

## Consequences

**Positive**
- Zero idle cost — no compute charges when no one visits the site.
- Free tier covers 1M Lambda requests + 1M API Gateway calls/month.
- IAM-based least-privilege: the Lambda role only has `dynamodb:UpdateItem`
  on the single counter table.
- Deployment is one `zip` + `terraform apply` — no AMIs, no patching.

**Negative**
- Cold starts (~200–400ms first hit) — acceptable because the counter is
  fetched asynchronously after page load.
- Logs are CloudWatch-only (vs. systemd/file logs on EC2).

## Alternatives Considered

- **EC2 with nginx + Flask** — rejected: always-on instance cost (~$7/month
  for t3.micro after free tier), patching burden, overkill for one endpoint.
- **Amplify Function / Vercel** — rejected: adds a non-AWS dependency,
  splits the cloud story.
- **Direct browser → DynamoDB via Cognito** — rejected: exposes IAM complexity
  to the frontend and still requires credential handling.
