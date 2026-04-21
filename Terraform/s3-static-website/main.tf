terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.41.0"
    }
    random = {
        source  = "hashicorp/random"
        version = "3.8.1"
  }
  }
}

provider "aws" {
  region = "ap-south-1"
}


provider "random" {
  
}

resource "random_id" "ran_id" {
  byte_length = 8

}

output "random_id_hex" {
  value = random_id.ran_id.hex
}

resource "aws_s3_bucket" "my_webapp_bucket" {
  bucket = "my-webapp-bucket-${random_id.ran_id.hex}"
}

resource "aws_s3_bucket_public_access_block" "my_webapp_bucket_public_access_block" {
  bucket = aws_s3_bucket.my_webapp_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "my_webapp_bucket_policy" {
  bucket = aws_s3_bucket.my_webapp_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = "*"
        Action = "s3:GetObject"
        Resource = "arn:aws:s3:::${aws_s3_bucket.my_webapp_bucket.id}/*"
      }
    ]
  })
  
}

resource "aws_s3_bucket_website_configuration" "my_webapp_website" {
  bucket = aws_s3_bucket.my_webapp_bucket.id
  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_object" "index_html" {
  bucket  = aws_s3_bucket.my_webapp_bucket.bucket
  source = "./index.html"
    key    = "index.html"
content_type = "text/html"
}

resource "aws_s3_object" "styles_css" {
  bucket  = aws_s3_bucket.my_webapp_bucket.bucket
  source = "./styles.css"
    key    = "styles.css"
content_type = "text/css"
}

output "website_url" {
  value = aws_s3_bucket.my_webapp_bucket.website_endpoint 
}