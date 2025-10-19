resource "aws_ecr_repository" "app_repo" {
  name = "devops-platform"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "devops-platform-ecr"
    Environment = var.environment
  }
}
