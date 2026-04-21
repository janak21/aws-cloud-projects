terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.41.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "my_ec2_instance" {
  ami           = "ami-0e12ffc2dd465f6e4"
  instance_type = "t3.micro"
  subnet_id = "subnet-0463e4a81e2266e24"

  tags = {
    Name = "MyEC2Instance"
  }
  
}