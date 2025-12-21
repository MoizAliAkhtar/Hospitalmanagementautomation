resource "aws_instance" "hospital_server" {
  ami           = "ami-0fe8bec493a81c7da"
  instance_type = "t3.micro"
  key_name      = "hospital-key"

  tags = {
    Name = "Hospital-Management-Server"
  }
}
