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

resource "aws_s3_bucket" "my_s3_bucket" {
  bucket = "my-unique-s3-bucket-${random_id.ran_id.hex}"
}

resource "aws_s3_object" "bucket_object" {
  bucket  = aws_s3_bucket.my_s3_bucket.bucket
  key     = "myfile.txt"
  content = "This is a sample file content for S3 object."
}