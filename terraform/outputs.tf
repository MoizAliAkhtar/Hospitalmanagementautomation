output "ec2_public_ip" {
  value = aws_instance.hospital_server.public_ip
}
