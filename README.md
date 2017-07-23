# Serverless ETL Demo

An example how to orchestrate multiple AWS lambda functions to do basic ETL process via AWS Step Functions.

To reproduce this demo:

1. Clone this repo to your local
2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
3. From Terminal, change your working directory to the cloned repo folder
4. Open up `Vagrantfile` and change all variables value below `# YOUR AWS ACCOUNT INFORMATION` line with:
	- `AWS_KEY` with your ***AWS Access Key ID***
	- `AWS_SECRET` with your ***AWS Secret Access Key***
	- `DBURL` with your complete ***PostgresSQL*** endpoint (e.g `postgres://user:pass@i-love-erdinger.rds.amazonaws.com:5432/dbname`)
	- `AWSID` with your ***AWS account ID***
	- `TZONE` with your Linux time zone preference (e.g `Asia/Jakarta`)
5. Run `vagrant up --provision` command to build the dev VM
6. Run `vagrant ssh` to enter the dev VM
7. Run `cd /vagrant` to change your working directory to cloned repo on dev VM
8. Run `sls deploy`
9. Hit the API endpoint (that you get from info output after sucessfull deployment) with content from `samplereq.json`

