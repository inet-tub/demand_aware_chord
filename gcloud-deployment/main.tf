terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file("credentials.json")

  project = var.project
  region  = var.region
  zone    = var.zone
}

locals {
  name_prefix = "k"
  ssh_keys    = join("\n", [for key in var.ssh_keys : "${key.user}:${key.keymaterial}"])
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}
resource "google_compute_subnetwork" "subnet" {
  name          = "${local.name_prefix}-subnetwork"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc_network.id
}

data "google_compute_image" "container_optimized_image" {
  # Use a container optimized image
  # See a list of all images : https://console.cloud.google.com/compute/images
  family  = "ubuntu-2004-lts"
  project = "ubuntu-os-cloud"
}


resource "google_compute_instance" "master" {
  name         = "${local.name_prefix}-master"
  machine_type = var.machine_type

  allow_stopping_for_update = true
  tags                      = []
  metadata = {
    ssh-keys = local.ssh_keys
  }
  zone = var.zone

  boot_disk {
    initialize_params {
      image = data.google_compute_image.container_optimized_image.self_link
    }
  }

  network_interface {
    network_ip = "10.0.0.2"
    subnetwork = google_compute_subnetwork.subnet.name
    dynamic "access_config" {
      for_each = var.public_access ? ["active"] : []
      content {}
    }
  }
  metadata_startup_script = templatefile("${path.module}/setup.tpl", {})
}

resource "google_compute_firewall" "ssh-rule" {
  name    = "${local.name_prefix}-rule-ssh"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  dynamic "allow" {
    for_each = var.public_access ? ["80"] : []
    content {
      protocol = "tcp"
      ports    = [allow.value]
    }
  }

  source_ranges = ["0.0.0.0/0"]
}

output "public_ip" {
  value = google_compute_instance.master.network_interface.0.access_config.0.nat_ip
}