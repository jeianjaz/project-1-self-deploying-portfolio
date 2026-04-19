# Architecture Decision Records

This directory captures the *why* behind key technical choices in CloudDeck.
Each ADR is a short, immutable record of a decision: what we chose, why,
and what we gave up.

Format follows [Michael Nygard's ADR template](https://github.com/joelparkerhenderson/architecture-decision-record).

| ID | Title | Status |
|----|-------|--------|
| [001](./001-dynamodb-over-rds.md) | Use DynamoDB over RDS for Visitor Counter | Accepted |
| [002](./002-cloudfront-oac-over-signed-urls.md) | Use CloudFront with OAC over Signed URLs | Accepted |
| [003](./003-lambda-apigateway-over-ec2.md) | Use Lambda + API Gateway over EC2 | Accepted |
| [004](./004-checkov-in-ci.md) | Run Checkov in CI Before Apply | Accepted |

## Adding a new ADR

1. Copy `000-template.md` to `NNN-slug.md` (next number).
2. Fill in Context, Decision, Consequences, Alternatives.
3. Set status to `Proposed`, open a PR, discuss, merge with status `Accepted`.
4. Never edit an accepted ADR — supersede it with a new one.
