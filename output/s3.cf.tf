

resource "aws_s3_bucket" "foo_bucket" {
  bucket = "foo"
  acl    = "public-read"
}