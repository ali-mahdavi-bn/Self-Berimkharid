from minio import Minio
from minio.error import S3Error
import uuid
import tempfile
import io
#
from Berimkharid.local_settings import minioAddress, minioAccessKey, minioSecretKey, minioBucketNames

minio_client = Minio(
    minioAddress,
    access_key=minioAccessKey,
    secret_key=minioSecretKey,
    secure=False,
)


def get_image_url_from_minio(bucket_name, object_name, expires=60):
    try:
        url = minio_client.presigned_get_object(bucket_name, object_name, expires=expires)
        return url
    except Exception as err:
        print(err)


def upload_image_to_minio(file, type, format, length):
    fileName = str(uuid.uuid4())
    bucketName = minioBucketNames[type]
    path = fileName + '.' + format
    try:
        minio_client.put_object(bucketName, path, io.BytesIO(file), length, content_type="application/octet-stream", )
        return {'bucketName': bucketName, 'path': path}
    except Exception as err:
        print(err)
        return False
