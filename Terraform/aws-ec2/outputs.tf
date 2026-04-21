output "aws_instance_private_ip" {
  value = aws_instance.my_ec2_instance.private_ip
}