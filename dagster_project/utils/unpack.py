from minio import Minio
from minio.error import S3Error
import magic
from io import BytesIO
FOLDER_PATH='Cit0/Cit0day.in_special_for_xss.is/Cit0day Prem [_special_for_xss.is]/'


def unrar(object: BytesIO) -> List[]:

# Function to process all objects in the specified bucket
def process_objects(bucket, minio_client, mime_detector):
    # List objects in the bucket
    try:
        objects = minio_client.list_objects(bucket, prefix=FOLDER_PATH)
        for obj in objects:
            # Get the object
            if not obj.object_name.endswith('/'):
                response = minio_client.get_object(bucket, obj.object_name)
                # Use BytesIO to handle the object in memory
                data = BytesIO(response.data)
                
                # Use 'python-magic' to determine the MIME type
                mime_type = mime_detector.from_buffer(data.getvalue())
                
                # Print details
                print(f'###\nObject Name: {obj.object_name}, \nMIME Type: {mime_type}')
                
                # Close the stream
                data.close()
                response.close()
    except S3Error as err:
        print("S3 Error:", err)

def main():
    import os 
    # MinIO credentials and configuration
    minio_url = os.getenv("S3_ENDPOINT")
    aws_access_key_id = os.getenv("S3_ACCESS_KEY")
    aws_secret_access_key = os.getenv("S3_SECRET_KEY")
    bucket_name = 'leaks'

    # Connect to MinIO
    minio_client = Minio(
        "nas.reinthal.me:9000",
        access_key=aws_access_key_id,
        secret_key=aws_secret_access_key,
        secure=False
    )

    # Initialize magic for MIME type detection
    mime_detector = magic.Magic(mime=True)
    process_objects(bucket_name,minio_client,mime_detector)

if __name__ == '__main__':
    main()