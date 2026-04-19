# ADR-001: Use DynamoDB over RDS for Visitor Counter

- **Status:** Accepted
- **Date:** 2026-04-19
- **Deciders:** Jeian Jasper

## Context

CloudDeck needs persistent storage for a single integer: the site's
visitor count. The counter is incremented once per page view, read
once per page view, and never queried relationally. Traffic is
unpredictable but low-volume (tens to hundreds of requests/day).

## Decision

Use **Amazon DynamoDB** with a single-item table keyed by
`id = "visitor_count"`.

## Consequences

**Positive**
- Pay-per-request pricing → $0.00 on free tier at current traffic.
- No VPC, subnet, or security group required → simpler Terraform.
- Sub-10ms reads/writes match the latency budget of a CDN-fronted site.
- Scales to millions of writes without operator action.

**Negative**
- No SQL / no joins — acceptable because the counter has no relational needs.
- Eventual consistency by default (we use strongly consistent reads for accuracy).

## Alternatives Considered

- **Amazon RDS (MySQL/PostgreSQL)** — rejected: requires a VPC, subnet
  group, and an always-on instance (~$15/month min). Massive over-engineering
  for one integer.
- **S3 object with a JSON counter** — rejected: no atomic increment primitive;
  concurrent requests would race.
- **In-memory Lambda counter** — rejected: Lambda is stateless; state would
  be lost on cold starts.
