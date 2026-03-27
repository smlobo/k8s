terraform {
  required_version = ">= 1.5.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

provider "kubernetes" {
  config_path = pathexpand("~/.kube/config")
  # If needed for MicroK8s, use:
  # config_path = "/var/snap/microk8s/current/credentials/client.config"
}

# resource "kubernetes_namespace" "demo" {
#   metadata {
#     name = "default"
#   }
# }

variable "namespace" {
  type = string
  default = "default"
}

resource "kubernetes_deployment" "nginx" {
  metadata {
    name      = "nginx-pv-deployment-tf"
    # namespace = kubernetes_namespace.demo.metadata[0].name
    namespace = var.namespace
    labels = {
      app = "nginx-server-tf"
    }
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "nginx-server-tf"
      }
    }

    template {
      metadata {
        labels = {
          app = "nginx-server-tf"
        }
      }

      spec {
        container {
          name  = "nginx"
          image = "nginx:1.27-alpine"

          port {
            container_port = 80
          }
          volume_mount {
            mount_path = "/usr/share/nginx"
            name = "nginx-pv-storage-tf"
          }
        }
        volume {
          name = "nginx-pv-storage-tf"
          persistent_volume_claim {
            claim_name = "local-pvc-srv-k8ssandra"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "nginx" {
  metadata {
    name      = "nginx-pv-service-tf"
    # namespace = kubernetes_namespace.demo.metadata[0].name
    namespace = var.namespace
  }

  spec {
    selector = {
      app = "nginx-server-tf"
    }

    port {
      port        = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}
