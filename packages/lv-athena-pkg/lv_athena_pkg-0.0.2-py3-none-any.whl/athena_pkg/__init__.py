import pandas as pd
def ConnectToAthena(aws_access_key_id,aws_secret_access_key,s3_staging_dir,region_name):
    """Returns an instance to connect you to AWS Athena via pyAthena"""
    from pyathena import connect
    return connect(aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,s3_staging_dir=s3_staging_dir,region_name=region_name)