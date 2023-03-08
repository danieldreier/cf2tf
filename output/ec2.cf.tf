
resource "aws_instance" "ec2_instance" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  key_name      = "my-ec2-key"
 
  block_device_mappings {
    device_name = "/dev/sdb"
    ebs {
      volume_size = 10
      volume_type = "gp2"
      delete_on_termination = true
    }
  }

  network_interface {
    device_index = 0
    delete_on_termination = true
    network_interface_id = aws_subnet.subnet_abc123.id
    associate_public_ip_address = true
  }
}