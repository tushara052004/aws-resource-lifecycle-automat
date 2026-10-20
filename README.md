# AWS Resource Lifecycle Automator

Python automation that cleans up idle AWS resources (EC2 and RDS) using boto3, with an AWS Lambda entry point that runs across all regions. Tested locally against a mocked AWS using moto, so no real AWS account is needed.

## What it does
- **EC2 (`ec2.py`)**
  - Stops running instances, unless tagged `excludepower=true`
  - Terminates instances that have no `user` tag
  - Deletes unattached (available) EBS volumes
  - Deletes snapshots older than a set number of days
- **RDS (`rds.py`)**
  - Stops database instances, unless tagged `excludepower=true`
- **Lambda (`awsLambda.py`)**
  - Loops through every AWS region and runs the EC2 and RDS cleanup in each

## Testing without a real AWS account
The `test_*.py` files use [moto](https://github.com/getmoto/moto) to simulate AWS:

| File | What it checks |
|------|----------------|
| `test_fake_aws.py` | EC2 stop/terminate rules and volume cleanup |
| `test_snapshots.py` | Snapshot lookup and deletion |
| `test_rds.py` | RDS stop rules and the `excludepower` tag |
| `test_lambda.py` | The full Lambda across multiple regions |

## How to run the tests
```
pip install boto3 "moto[ec2,rds]"
python test_fake_aws.py
python test_snapshots.py
python test_rds.py
python test_lambda.py
```

## Fixes I made to the starter code
- Added the missing snapshot lookup function so snapshot cleanup no longer crashes
- Fixed a counter that never increased
- Added the missing imports in `awsLambda.py`

## Warning
This tool terminates and deletes real resources. Do not run it on an AWS account that holds anything important. Test with moto first.

## Known limitations
- In `rds.py`, databases are stopped but never deleted
- Fake test credentials are used in the tests. No real keys are stored in this repo.
