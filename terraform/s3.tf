resource "aws_s3_bucket" "s3_projetofinal" {
  bucket = "s3-projetofinal-scaws"

  tags = {
    Name = "S3 Projeto Final"
  }
}

# resource "aws_s3_bucket_notification" "bucket_notification" {
#   bucket = aws_s3_bucket.s3_projetofinal.id

#   lambda_function {
#     lambda_function_arn = aws_lambda_function.lambda_lambdas3.arn
#     events              = ["s3:ObjectCreated:*"]
#   }
#   depends_on = [aws_lambda_function.lambda_lambdas3]
# }