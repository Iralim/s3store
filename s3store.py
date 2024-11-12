import argparse
import os.path
from minio import Minio
from minio.error import S3Error

# s3store.py -o HOST -k KEY -s SECRET -b BUCKET -f filename

parser = argparse.ArgumentParser(description='S3 Lagring')
parser.add_argument('-o', '--host', type=str, help="Host name", required=True) # Jag lämnade -o som du beskrev i uppgiften. Men kallade hela argument-namnet  --host
parser.add_argument('-k', '--key', type=str, help="Access key", required=True)
parser.add_argument('-s', '--secret', type=str, help="Secret key", required=True)
parser.add_argument('-b', '--bucket', type=str, help="Bucket name", required=True)
parser.add_argument('-f', '--file', type=str, help="Full filename", required=True)

args = parser.parse_args()


def main(host, key, secret, bucket, file):
    if not os.path.exists(file):
        parser.error("Could not find the file: %s" % file)

    client = Minio(
        host,
        access_key=key,
        secret_key=secret,
    )

    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)
    else:
        print(f"Bucket '{bucket}' already exists")

    client.fput_object(
        bucket, os.path.basename(file), file,
    )
    print(
        f" '{file}' is successfully uploaded as '{os.path.basename(file)}' to bucket '{bucket}'."
    )


if __name__ == "__main__":
    try:
        main(args.host, args.key, args.secret, args.bucket, args.file)
    except S3Error as exc:
        print("error occurred.", exc)

