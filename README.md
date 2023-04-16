# Connext Galxe Dashboard

## Usage
Since we use Elastic Container Service (ECS), it is required to build an docker image before pushing to the repository first. To do so, follow this instruction:
### 1. Setup AWS CLI
#### 1.1 Installation

#### 1.2 Authrization


### 2. Create docker repository
```sh
aws ecr create-repository --repository-name <repository-name> --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

### 3. Prepare docker image
#### 3.1 Docker login with AWS
```sh
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-id>.dkr.ecr.<region>.amazonaws.com
```


#### 3.1 Build a dockerfile
```sh
docker build --platform=linux/amd64 -t <container-name> -f <path-to-dockerfile> .
```

#### 3.2 Tag docker
```sh
docker tag <container-name>:latest <repository-url>:latest
```

#### 3.3 Push a docker
```sh
docker push <repository-url>:latest
```

### 4. Create a function
#### 4.1 Create an execution role
```sh
aws iam create-role --role-name <role-name> --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
```

#### 4.2 Create Lambda Function
```sh
aws lambda create-function --function-name <lambda-function-name> --package-type Image --code ImageUri=<repository-url>:latest --role arn:aws:iam::<aws-id>:role/<role-name-from-4.1>
```

### 5. Configure Environment variables
Configure `Environment variables` in a `Configuration` tab. Make sure to add the following variables:
- `DEBUG`: `true` if you wish the log to be verbose else `false`
- `ARBITRUMSCAN_APIKEYS`
- `BSCSCAN_APIKEYS`
- `GNOSISSCAN_APIKEYS`
- `OPTIMISTICSCAN_APIKEYS`
- `POLYGONSCAN_APIKEYS`
- `AWS_RDS_HOSTNAME`
- `AWS_RDS_USERNAME`
- `AWS_RDS_PASSWORD`

## Author
Chompakorn Chaksangchaichot