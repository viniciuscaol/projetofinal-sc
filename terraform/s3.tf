resource "aws_s3_bucket" "s3_projetofinal" {
  bucket = "s3-projetofinal-scaws"

  tags = {
    Name = "S3 Projeto Final"
  }
}