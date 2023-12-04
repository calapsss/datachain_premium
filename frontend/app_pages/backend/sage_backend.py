import time
import boto3
import sagemaker
import os
from sagemaker import get_execution_role
from sagemaker.automl import automl
from urllib.parse import urlparse
from dotenv import load_dotenv
import subprocess

class s3Setup():

    def __init__(self):
        load_dotenv()
        self.access_key, self.secret_access_key = os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY')

    #helper function to create s3 client

    def create_client(self):
        s3 = boto3.client(
            's3',
            aws_access_key_id= self.access_key,
            aws_secret_access_key=self.secret_access_key
        )
        return s3
    
    def list_bucket_contents(self,bucket_name):
        """
        prints files within bucket to ensure files are uploaded
        :param bucket_name: Bucket of files you want printed
        """

        # Create an S3 client with credentials
        s3 =self.create_client()

        key_list = []

        try:
            # List objects within the bucket
            response = s3.list_objects_v2(Bucket=bucket_name)

            # Check if the bucket is empty
            if 'Contents' not in response:
                print("The bucket is empty.")
                return

            # Print the names of the files in the bucket
            for item in response['Contents']:
                key_list.append(item['Key'])

        except Exception as e:
            print(f"Error accessing bucket {bucket_name}: {e}")
            return

        return key_list


    def upload_file_to_bucket(self,bucket_name, file_path, object_name=None):
        """
        Upload a file to an S3 bucket

        :param bucket_name: Bucket to upload to
        :param file_path: File path to upload
        :param object_name: S3 object name. If not specified, file_path is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_path

        # Create an S3 client with credentials
        s3 = self.create_client()

        #upload bucket
        try:
            s3.upload_file(file_path, bucket_name, object_name)
        except Exception as e:
            print(f"Error uploading file to bucket {bucket_name}: {e}")
            return False
        return True

class Autopilot():

    def __init__(self, name):
        load_dotenv()
        self.access_key, self.secret_access_key = os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = 'us-east-1'
        self.job_name = name
    
    #helper function to create s3 client
    def create_session(self):
        boto_session = boto3.Session(
        aws_access_key_id=self.access_key,
        aws_secret_access_key=self.secret_access_key,
        region_name= self.region_name  # specify your region
        )
        return boto_session
    
    def run_autopilot_job(self,role,bucketName,fileName,targetVariable,jobName):
        """
        runs autopilot

        :param role: aws role compatible with sagemaker
        :param bucketName: Bucket to pull data from
        :param fileName: file name of data
        :param targetVariable: variable you want to predict
        :param jobName: unique name of job that will be produced in AWS
        """


        # Initialize a Boto3 session with your AWS credentials
        boto_session = self.create_session()

        # Initialize the SageMaker session with the custom Boto3 session
        sagemaker_session = sagemaker.Session(boto_session=boto_session)

        # Define the S3 path to the data
        s3_input_data = f's3://{bucketName}/{fileName}'

        # Set up the Autopilot job
        autopilot_job = automl.AutoML(
        role=role,
        target_attribute_name=targetVariable,  # Replace with your target column
        sagemaker_session=sagemaker_session,
        max_candidates=10  # Specify the maximum number of candidates
    )

        # Start the Autopilot job with the specified job name
        autopilot_job.fit(inputs=s3_input_data, job_name=jobName, wait=False, logs=False)

        # The job is now running asynchronously
        print(f"Started Autopilot job: {jobName}")

        # Track the progress using the SageMaker client from the boto_session
        sm_client = boto_session.client('sagemaker')

        while True:
            job_response = sm_client.describe_auto_ml_job(AutoMLJobName=jobName)
            job_status = job_response['AutoMLJobStatus']
            job_secondary_status = job_response['AutoMLJobSecondaryStatus']
            print(f"Job status: {job_status}, secondary status: {job_secondary_status}")

            if job_status in ['Completed', 'Failed', 'Stopped']:
                break

            time.sleep(45)  # Wait for 45 seconds before checking again
    
    def extract_autopilot_product(self,jobName,localDir):
        """
        extracts all of the data, including notebooks, from the autopilot experiment created

        :param jobName: unique name of job that will be produced in AWS
        :param localDir: name of file you want to create to put all produced data in
        """

        # Initialize a Boto3 session with your AWS credentials
        boto_session = self.create_session()

        # Initialize the SageMaker client using the boto_session
        sagemaker_client = boto_session.client('sagemaker')
        s3_client = boto_session.client('s3')

        # Get the Autopilot job description
        job_description = sagemaker_client.describe_auto_ml_job(AutoMLJobName=jobName)

        # Retrieve the S3 URI for the output artifacts
        output_uri = job_description['OutputDataConfig']['S3OutputPath']

        # Parse the S3 URI
        parsed_url = urlparse(output_uri)
        bucket_name = parsed_url.netloc
        output_prefix = parsed_url.path.lstrip('/')

        # Create a local directory to store the downloaded files
        os.makedirs(localDir, exist_ok=True)

        # List and download the output files in the S3 URI
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=output_prefix)
        for content in response.get('Contents', []):
            file_key = content['Key']
            local_file_path = os.path.join(localDir, os.path.basename(file_key))
            #print(f"Downloading {file_key} to {local_file_path}...")
            s3_client.download_file(bucket_name, file_key, local_file_path)

        print("Download complete.")