import boto3
import time
import argparse
import threading
import datetime
import logging
import configparser


extend_visbilitytime = False
message_timeout = 100
process_completion = False

def move_message(sqs_queue,source_queue,destination_queue,batch_value,region,boolean_purge):
    global message_timeout
    global extend_visbilitytime
    global process_completion
    try:
        logging.debug("Successfully Created the client")
        sqs_messages = sqs_queue.receive_message(QueueUrl=source_queue, AttributeNames = ['ALL'],MaxNumberOfMessages=batch_value,VisibilityTimeout=message_timeout,WaitTimeSeconds=20)
        logging.debug("Processing the messages")
        while 'Messages' in sqs_messages:
            print("processing set of messages")
            extend_visbilitytime = False
            curr_time = datetime.datetime.now()
            timer_thread = threading.Thread(target=time_counter)
            timer_thread.start()
            logging.debug("Calling timer_Counter")
            for i in range (0,len(sqs_messages['Messages'])):
                print(sqs_messages['Messages'][i]['Body'])
                transfer_message = sqs_queue.send_message(QueueUrl=destination_queue,MessageBody=sqs_messages['Messages'][i]['Body'])
                if(len(transfer_message['MessageId'])==0):
                    logging.debug("seems couldn't message send")
                elif boolean_purge == False:
                    sqs_delete_message = sqs_queue.delete_message(QueueUrl=source_queue,ReceiptHandle=sqs_messages['Messages'][i]['ReceiptHandle'])
                    print(sqs_delete_message)
                    if ((sqs_delete_message['ResponseMetadata']['HTTPStatusCode'])==200):
                        logging.debug("successfully deleted the message ..proceeding further")
                    else:
                        logging.debug("didnt delete the message")
                else:
                    logging.debug("message send successfully and removed from old queue, continuing message processing")
                    continue

            if(extend_visbilitytime == True):
                logging.debug("extending the visibility timeout")
                updated_timeout = (datetime.datetime.now()-a).total_seconds()
                message_timeout = int(updated_timeout)

            sqs_messages = sqs_queue.receive_message(QueueUrl=source_queue, AttributeNames=['ALL'],MaxNumberOfMessages=10,VisibilityTimeout=message_timeout,WaitTimeSeconds=20)
        if boolean_purge == True:
            purgeing_queue = sqs_queue.purge_queue(QueueUrl=source_queue)
            if(purgeing_queue['ResponseMetadata']['HTTPStatusCode']==200):
                logging.debug("Successful Purgeing")
        logging.debug("processing completed")
        print("processing completed")
        process_completion = True
    except Exception as exp:
        logging.error(exp)
    return process_completion

def time_counter():
    global extend_visbilitytime
    time.sleep(100)
    extend_visbilitytime = True
    logging.debug("changed the extend_visbilitytime to True")

def setup_logging():
    log_filename = str(datetime.datetime.today().strftime("%Y-%m-%d")) + ".log"
    logging.basicConfig(filename=log_filename, level=logging.DEBUG)
    logging.debug("Initiating the Run")

def run_from_cli():
    parser = argparse.ArgumentParser(description="Move messages between SQS queues.")
    parser.add_argument("-p","--poll",help="Poll messages from the source queue without deleting from source queue",action="store_true")
    parser.add_argument("-s", "--source", help="Source queue name", required=True)
    parser.add_argument("-d", "--dest", help="Destination queue name", required=False)
    parser.add_argument("-pr","--purge", help="Purge the destination Queue",action="store_true")
    parser.add_argument("-r","--region",type=str,help="The queue Regions in the order of source destination",required=True)
    parser.add_argument("-b","--batch",type=int,help="The number of messages to request each iteration 10 maximum",required=False,default=10)
    parser.add_argument("-pf", "--profile", help="profile", required=True,default='default')
    parser.add_argument("-f", "--filepath", help="profile", required=True,default='default')
    args = parser.parse_args()
    print(args)
    if not args.dest or not args.source:
            parser.error("-d and -s argument are required for processing")
    setup_logging()
    source_queue = args.source
    destination_queue = args.dest
    batch_value = args.batch
    source_region = args.region
    boolean_purge = args.purge
    filepath = args.filepath
    config = configparser.ConfigParser()
    config.read(filepath)
    profile = args.profile
    print(profile)
    aws_accesskey = config[profile]['aws_access_key_id']
    aws_secretkey = config[profile]['aws_secret_access_key']
    logging.debug("Calling move_message with the required params")
    logging.debug(args)
    print(aws_accesskey)
    sqs_queue = boto3.client('sqs',aws_access_key_id=aws_accesskey, aws_secret_access_key=aws_secretkey, region_name=source_region)
    #move_message(sqs_queue,source_queue,destination_queue,batch_value,source_region,boolean_purge)

if __name__ == "__main__":
    run_from_cli()
