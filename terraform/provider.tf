provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      projeto = "SCADA"
      dono    = "Vinicius"
    }
  }
}
