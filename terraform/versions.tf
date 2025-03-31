terraform {
  required_version = ">= 1.11.2"

  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.6.0"
    }
  }
}
