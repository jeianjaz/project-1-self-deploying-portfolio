# ADR-004: Run Checkov in CI Before Terraform Apply (Not After)

- **Status:** Accepted
- **Date:** 2026-04-19
- **Deciders:** Jeian Jasper

## Context

CloudDeck's Terraform provisions IAM, S3, CloudFront, Lambda, and
DynamoDB — all resources where a misconfiguration (public bucket,
overly permissive role, missing encryption) can become a security
incident. We need automated guardrails that block bad config from
reaching AWS.

## Decision

Run **Checkov** as the first stage of the GitHub Actions CI/CD
pipeline, **before** `terraform validate` and `terraform apply`. The
pipeline fails closed on any `HIGH` or `CRITICAL` finding.

## Consequences

**Positive**
- Misconfigurations are caught at PR time, not after deployment.
- Free, open-source, 1000+ built-in AWS policies.
- Same scanner runs locally (`checkov -d terraform/`) — devs can pre-check
  before pushing.
- Produces a documented security posture: every `skip` is justified inline.

**Negative**
- ~20–30s added to every pipeline run.
- Some policies are opinionated (e.g. `CKV_AWS_18` S3 access logging for a
  portfolio site) and must be explicitly skipped with justification.

## Alternatives Considered

- **Post-deploy AWS Config rules** — rejected: detects issues *after* they
  exist in production. Shifts the cost of fixing left → right.
- **`terraform plan` + manual review** — rejected: doesn't scale, relies on
  reviewer remembering every security rule.
- **tfsec** — considered: similar tool; Checkov chosen for broader policy
  coverage (IaC + Dockerfile + Kubernetes) — useful for Projects 2 and 3.
