terraform { 
  required_providers { 
    aws = { 
      source  = "hashicorp/aws" 
      version = "~> 6.0" 
    } 
  } 
} 

provider "aws" { 
  region = "us-east-1" 
} 

resource "aws_instance" "experiment_instance" { 
  ami           = "ami-0c7217cdde317cfec" # Sample ID
  instance_type = "t2.micro" 
  
  tags = { 
    Environment = "Production" 
  } 
} 

output "hello_world" { 
  value = "Hello, world from Terraform!" 
}
