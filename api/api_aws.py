import json
from dotenv import load_dotenv, dotenv_values
import boto3
import os

env=".env" # 執行環境
load_dotenv(override=True)



class Aws_s3_api():
    def __init__(self):
        self.aws_client = boto3.client(
            's3',
            aws_access_key_id=dotenv_values(env)["access_key"],
            aws_secret_access_key=dotenv_values(env)["secret_access_key"],
        )
        self.bucket="message-board-yin"
        
    def get_data_url(self, img):
        img_url=self.aws_client.generate_presigned_url(
            "get_object",
            Params={"Bucket":self.bucket, "Key":img},
            ExpiresIn=6000
        )
        return img_url
    
    def upload_data(self, file, type, index):
        img_type='image/'+type
        filename='img'+str(index)+"."+type
        self.aws_client.put_object(Body=file, 
                                   Bucket=self.bucket, 
                                   Key=filename,
                                   ContentType=img_type
                                   )
        return filename

    def upload_json_data(self, file, filename):
        self.aws_client.put_object(Body=json.dumps(file), 
                                   Bucket=self.bucket, 
                                   Key=filename,
                                #    ContentType=img_type
                                   )
        return filename

    def delete_data(self):
        self.aws_client.delete_object(Bucket=self.bucket, Key='test.txt')
        return 0
    def delete_all_data(self):
        resp=self.aws_client.list_objects(Bucket=self.bucket)
        for index in resp["Contents"]:
            self.aws_client.delete_object(Bucket=self.bucket, Key=index["Key"])
        return 0
