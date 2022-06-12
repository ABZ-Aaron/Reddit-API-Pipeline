

output "redshift_cluster_hostname" {
  description = "ID of the Redshift instance"
  value       = replace(
      aws_redshift_cluster.redshift.endpoint,
      format(":%s", aws_redshift_cluster.redshift.port),"",
  )
}

output "redshift_port" {
    description = "Port of Redshift cluster"
    value = aws_redshift_cluster.redshift.port
}

output "redshift_password" {
    description = "Password of Redshift cluster"
    value = var.db_password
}

output "redshift_username" {
    description = "Username of Redshift cluster"
    value = aws_redshift_cluster.redshift.master_username
}

output "redshift_role" {
    description = "Role assigned to Redshift"
    value = aws_iam_role.redshift_role.name
}

data "aws_caller_identity" "current" {}
output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "aws_region" {
    description = "Region set for AWS"
    value = var.aws_region
}