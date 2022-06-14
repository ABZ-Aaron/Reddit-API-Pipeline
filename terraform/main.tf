terraform {
    required_version = ">= 1.2.0"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 4.16"
        }
    }
}

# Configure AWS provider
provider "aws" {
    region = var.aws_region
}

# Configure redshift cluster. This will fall under free tier as of June 2022.
resource "aws_redshift_cluster" "redshift" {
  cluster_identifier = "redshift-cluster-pipeline"
  skip_final_snapshot = true # must be set so we can destroy redshift with terraform destroy
  master_username    = "awsuser"
  master_password    = var.db_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  publicly_accessible = "true"
  iam_roles = [aws_iam_role.redshift_role.arn]
  vpc_security_group_ids = [aws_security_group.sg_redshift.id]
  
}

# Confuge security group for Redshift allowing all inbound/outbound traffic
 resource "aws_security_group" "sg_redshift" {
  name        = "sg_redshift"
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

# Create S3 Read only access role. This is assigned to Redshift cluster so that it can read data from S3
resource "aws_iam_role" "redshift_role" {
  name = "RedShiftLoadRole"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
}

# Create S3 bucket
resource "aws_s3_bucket" "reddit_bucket" {
  bucket = var.s3_bucket
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

# Set access control of bucket to private
resource "aws_s3_bucket_acl" "s3_reddit_bucket_acl" {
  bucket = aws_s3_bucket.reddit_bucket.id
  acl    = "private"
}
      
