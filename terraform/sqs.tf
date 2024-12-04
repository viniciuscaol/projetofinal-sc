resource "aws_sqs_queue" "sqs_projetofinal" {
  name                       = "sqs-projetofinal-scaws"
  visibility_timeout_seconds = 300
  # menssage_retention_seconds = 86400
  delay_seconds = 0

  tags = {
    Name = "SQS Projeto Final"
  }
}

resource "aws_sqs_queue_policy" "sqs_policy" {
  queue_url = aws_sqs_queue.sqs_projetofinal.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.sqs_projetofinal.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.sns_projetofinal.arn
          }
        }
      }
    ]
  })
}