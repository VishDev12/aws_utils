"""Script to upload files to S3 and generate a list of the object URLs to a CSV.

AWS CLI v2
"""
import argparse
import subprocess
import pandas as pd

if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("--source")
    arg_parse.add_argument("--bucket")
    arg_parse.add_argument("--key")
    arg_parse.add_argument("--column_name")
    arg_parse.add_argument("--acl", default="public-read-write")

    args = arg_parse.parse_args()
    args_dict = args.__dict__

    bucket = args_dict["bucket"]
    key = args_dict["key"]
    key = key.strip("/")
    dest_key = "s3://" + bucket + "/" + key + "/"

    source = args_dict["source"]
    column_name = args_dict["column_name"]
    acl = args_dict["acl"]

    input("\n\nReading from {} and writing to {}\n\nConfirm? (Press Ctrl + C to exit)".format(source, dest_key))
    check = subprocess.call("aws s3 cp {} {} --recursive --acl {} --no-progress > {}.txt".format(source, dest_key, acl, key), shell=True)

    with open("{}.txt".format(key), "r") as r:
        ls = r.readlines()
    
    for i, j in enumerate(ls):
        ls[i] = "https://{}.s3.amazonaws.com/{}/".format(bucket, key) + j.rstrip().split(" ")[-1].split("/")[-1]

    df = pd.DataFrame({column_name: ls})
    df.to_csv("{}.csv".format(key))
