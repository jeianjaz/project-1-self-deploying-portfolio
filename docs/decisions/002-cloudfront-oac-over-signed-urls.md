# ADR-002: Use CloudFront with Origin Access Control (OAC) over Signed URLs

- **Status:** Accepted
- **Date:** 2026-04-19
- **Deciders:** Jeian Jasper

## Context

CloudDeck serves a public portfolio site from an S3 bucket via
CloudFront. We need to (a) keep the S3 bucket private (no public
`GetObject`), (b) serve content over HTTPS globally with low latency,
and (c) avoid any per-user access control — the site is public.

## Decision

Use **CloudFront with Origin Access Control (OAC)**. The S3 bucket
policy only grants `s3:GetObject` to the CloudFront distribution's
service principal, scoped by `aws:SourceArn`.

## Consequences

**Positive**
- S3 bucket is never publicly accessible; Checkov `CKV_AWS_53/54/55/56` pass.
- CloudFront handles TLS termination, HTTP→HTTPS redirect, and edge caching.
- OAC replaces legacy OAI and supports SigV4 for future KMS-encrypted origins.
- Zero per-request signing cost and no URL expiry logic to maintain.

**Negative**
- Any region/product change to the bucket requires the distribution to be
  updated — tight coupling accepted for this use case.

## Alternatives Considered

- **CloudFront Signed URLs/Cookies** — rejected: introduces expiring URLs
  and a key-pair to rotate. Designed for paid/private content, not public assets.
- **Public S3 bucket with website hosting** — rejected: exposes bucket
  contents directly, fails security scans, no HTTPS on bucket endpoints.
- **Legacy Origin Access Identity (OAI)** — rejected: AWS recommends OAC
  for all new distributions; OAI is in maintenance mode.
