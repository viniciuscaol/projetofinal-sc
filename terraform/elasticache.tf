resource "aws_elasticache_cluster" "elasticache_projetofinal" {
  cluster_id           = "elasticache-projetofinal-scaws"
  engine               = "redis"
  node_type            = "cache.t2.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379

  tags = {
    Name = "Elasticache Projeto Final"
  }
}