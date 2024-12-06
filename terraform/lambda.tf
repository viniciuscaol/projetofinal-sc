resource "aws_lambda_function" "lambda_s3" {
  filename         = "../lambdas/lambdas3/lambda_function.zip"
  function_name    = "lambdas3"
  role             = "arn:aws:iam::434876288613:role/ProjetoFinal"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.13"
  source_code_hash = filebase64sha256("../lambdas/lambdas3/lambda_function.zip")
}

resource "aws_lambda_permission" "s3" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_s3.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.s3_projetofinal.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.s3_projetofinal.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_s3.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.s3]
}


resource "aws_lambda_function" "lambda_sns" {
  filename         = "../lambdas/lambdasns/lambda_function.zip"
  function_name    = "lambdasns"
  role             = "arn:aws:iam::434876288613:role/ProjetoFinal"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.13"
  source_code_hash = filebase64sha256("../lambdas/lambdasns/lambda_function.zip")
}

resource "aws_lambda_permission" "lambada_sns" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_sns.function_name
  principal     = "sns.amazonaws.com"
  # source_arn    = aws_sns_topic.topic.arn
}