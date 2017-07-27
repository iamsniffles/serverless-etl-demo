# Serverless ETL Demo

An example how to trigger a lambda function via an API Gateway which will execute a StepFunction to do a basic ETL process based on JSON input.

## How To

To reproduce this demo:

1. Clone this repo to your local
2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
3. From Terminal, change your working directory to the cloned repo folder
4. Open up `Vagrantfile` and change all variables value below `# YOUR AWS ACCOUNT INFORMATION` line with:
	- `AWSID` with your ***AWS account ID***
	- `REG` with your ***AWS Region*** preference
	- `AWS_KEY` with your ***AWS Access Key ID***
	- `AWS_SECRET` with your ***AWS Secret Access Key***
	- `S3BUCKET` with your ***S3 bucket*** name preference
	- `DBURL` with your complete ***PostgresSQL*** endpoint (e.g `postgres://user:pass@i-love-erdinger.rds.amazonaws.com:5432/dbname`)
	- `API_KEY` with phrase to secure your API endpoint
	- `TZONE` with your Linux time zone preference (e.g `Asia/Jakarta`)
5. Run `vagrant up --provision` command to build the dev VM
6. Run `vagrant ssh` to enter the dev VM
7. Run `cd /vagrant` to change your working directory to cloned repo on dev VM
8. Run `sls deploy --stage dev`
9. Hit the API endpoint (that you get from info output after successful deployment) with content from `samplereq.json`
10. On successful hit you will get response code `200` and message `Ingestion process triggered!`

## ETL Process

The process will extract `samplereq.json` content and devide it into three main object.

- **Event**
- **Charge**
- **Card**

There's no need to define target tables on your database. The target tables will be created during ingestion process if not exists yet (thanks to [dataset](https://dataset.readthedocs.io/en/latest/) package!).

*For more information about the `samplereq.json`, please refer to [this page](https://stripe.com/docs/api#charge_object).*

## Data Model

If you see your database after a successful API hit, there are 5 tables there.

- `event`
- `charge`
- `cc`
- `event_map`
- `event_raw`

`event`, `charge`, and `cc` are representation of three main objects mentioned before. Those three tables are mapped by `event_map` table. `event_raw` table contains flattened `samplereq.json`. `event_raw` table was created to facilitate type of data analyst who would like to see all data into one table whatever it takes.
