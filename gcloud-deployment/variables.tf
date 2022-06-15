variable "project" {
  type = string
  default = "cc-tub"
}
variable "ssh_keys" {
  type = list(object({
    keymaterial = string
    user        = string
  }))
  description = "list of public ssh keys that have access to the VMs"
  default = [
    {
      user        = "k"
      keymaterial = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC8xRrWR/oOFBoBfcz08gzQVBKaD1/hBBSVmHX3AAGIKS5Kc5N4qoy1kdd2TT84BObZ2CN5V7nCXXuxTA5MQESan57CEmbpGHKuDuwsvVPgq8s3xEH4dSM4GG+A/wV/5tgc1DSbF2kk7YWQdf/C3HoHDajmexumuDKq2RUO+Ckip0Y5rjRJLpc3dQ0jZ4Xd26d4siyLNh6D1qf/HjifGxKIb+BNhSZLrFH1v29vFLPmGvl8/VyOvuNFF/JMiAuTThWTXrQtgXYxpkux594cb4OgFQ36MnQdh2BSyvNjul46TZnE5xat5/lPxBsXD9Vjb8B70t48AudA61uTGfxxVgiGpRQ8MTxKhGKEm333RKmXx+RVdOXTO0/mDXtK0VdTQyFK7aWfxemXkoHUCMT+PVdifhvW077BD7b/fNHA2hNPvoN7gFvwqLDff/fkLgQufGYaujGUikXkaaAdfFTTLfkU7R7+L/A/5vVfKL//bThniqN2p6BwahfK0Pe7taZh25N4ZKXbiCZpcnsiNCviLiCx7+mE9F87woXIPhFSsLqrXPOLe902l8EQH+QCme4dvMZDKODqCOsq3T3Vn0qeMeMzvUBYiV94pBP2Rbmzrrklkzm+x6qnvjHHPrRnvIRKD6YYhXjkThXmvWEgTaXKxNG3OaHSv3Ukpgz/Viufqpy5fw== k"
    }  
]
}
variable "public_access" {
  type    = bool
  default = true
}

variable "region" {
  type    = string
  default = "europe-west3"
}
variable "zone" {
  type    = string
  default = "europe-west3-a"
}
variable "machine_type" {
  type        = string
  default     = "e2-standard-8"
  description = "The Machine Type used for all VMs"
}