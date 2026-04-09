data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/visitor_counter.py"
  output_path = "${path.module}/../lambda/visitor_counter.zip"
}

resource "aws_lambda_function" "visitor_counter" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${var.project_name}-visitor-counter"
  role             = aws_iam_role.lambda_role.arn
  handler          = "visitor_counter.lambda_handler"
  runtime          = "python3.12"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.visitor_counter.name
    }
  }

  tags = {
    Name = "${var.project_name}-visitor-counter"
  }
}

