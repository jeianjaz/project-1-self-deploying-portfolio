data "archive_file" "cost_lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/cost_dashboard.py"
  output_path = "${path.module}/../lambda/cost_dashboard.zip"
}

resource "aws_lambda_function" "cost_dashboard" {
  filename         = data.archive_file.cost_lambda_zip.output_path
  function_name    = "${var.project_name}-cost-dashboard"
  role             = aws_iam_role.lambda_role.arn
  handler          = "cost_dashboard.lambda_handler"
  runtime          = "python3.12"
  source_code_hash = data.archive_file.cost_lambda_zip.output_base64sha256
  timeout          = 15

  tags = {
    Name = "${var.project_name}-cost-dashboard"
  }
}