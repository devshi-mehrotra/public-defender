# ==================================================================================
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ==================================================================================
#
# translatevideo.py
# by: Rob Dachowski
# For questions or feedback, please contact robdac@amazon.com
# 
# Purpose: This code drives the process to create a transription job, translate it into another language,
#          create subtitles, use Amazon Polly to synthesize an alternate audio track, and finally put it all together
#          into a new video.
#
# Change Log:
#          6/29/2018: Initial version
#
# ==================================================================================


import argparse
from transcribeUtils import *
from srtUtils import *
from vttUtils import *
import time
# from videoUtils import *
from audioUtils import *

s3_client = boto3.client('s3')

def main(event, context):  
    print(event)
    jobName = event["detail"]["TranscriptionJobName"]
    region = "us-east-1"
    print(jobName)
    response = getTranscriptionJobStatus(jobName, region)
    print(response)
    transcriptFileUri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    print(transcriptFileUri)
    transcript = getTranscript(transcriptFileUri)
    print(transcript)

    splitJobName = jobName.split("_")
    print(splitJobName)
    bucket = splitJobName[2]
    print("bucket: {}".format(bucket))
    transcribed_path = '/tmp/' + "transcribed-" + splitJobName[-1][:-4] + ".VTT"
    print("transcribed path: {}".format(transcribed_path))
    aws_transcribed_path = '/'.join(splitJobName[3:-1]) + "/transcribed-" + splitJobName[-1][:-4] + ".VTT"
    print("aws transcribed path: {}".format(aws_transcribed_path))


    # Create the VTT File for the original transcript and write it out.  
    writeTranscriptToVTT(transcript, 'en', transcribed_path)  
    s3_client.upload_file(transcribed_path, '{}transcribed'.format(bucket), aws_transcribed_path)    	
    #s3_client.upload_file(transcribed_path, '{}transcribed'.format(bucket), aws_transcribed_path, ExtraArgs={'ACL':'bucket-owner-full-control'}) 


def transcribe_video(video_path, transcribed_path, region, bucket):
    # Create Transcription Job
    response = createTranscribeJob(region, bucket + "/", video_path)

    # loop until the job successfully completes
    print( "\n==> Transcription Job: " + response["TranscriptionJob"]["TranscriptionJobName"] + "\n\tIn Progress"),

    # while( response["TranscriptionJob"]["TranscriptionJobStatus"] == "IN_PROGRESS"):
    #     print( "."),
    #     time.sleep( 30 )
    #     response = getTranscriptionJobStatus( response["TranscriptionJob"]["TranscriptionJobName"], region )

    # print( "\nJob Complete")
    # print( "\tStart Time: " + str(response["TranscriptionJob"]["CreationTime"]) )
    # print( "\tEnd Time: "  + str(response["TranscriptionJob"]["CompletionTime"]) )
    # print( "\tTranscript URI: " + str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) )

    # # Now get the transcript JSON from AWS Transcribe
    # transcript = getTranscript( str(response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]) ) 
    # print(transcript)
    # # print( "\n==> Transcript: \n" + transcript)

    # # Create the VTT File for the original transcript and write it out.  
    # writeTranscriptToVTT(transcript, 'en', transcribed_path)  
    # s3_client.upload_file(transcribed_path, '{}transcribed'.format(bucket), transcribed_path[5:])    	



	
