output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.website.id
}

#ARN = AMAZON RESOURCE NAME - UNIQUE ID FOR EVERY AWS RESOURCE
output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.website.arn
}

output "s3_website_endpoint" {
  description = "S3 static website endpoint"
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name (your website URL)"
  value       = aws_cloudfront_distribution.website.domain_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.website.id
}

output "api_gateway_url" {
  description = "API Gateway URL for visitor counter"
  value       = "${aws_apigatewayv2_api.visitor_counter.api_endpoint}/count"
}
