from datetime import datetime
import json
import queue
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()

from attendees.models import AccountVO

def update_account_vo(ch, method, properties, body):
# Declare a function to update the AccountVO object (ch, method, properties, body)
    data = json.loads()
#   content = load the json in body
    first_name = data["first_name"]
#   first_name = content["first_name"]
    last_name = data["last_name"]
#   last_name = content["last_name"]
    email = data["email"]
#   email = content["email"]
    is_active = data["is_active"]
#   is_active = content["is_active"]
    updated_string = data["updated"]
#   updated_string = content["updated"]
    updated = datetime.fromisoformat(updated_string)
#   updated = convert updated_string from ISO string to datetime
#   if is_active:
    if data["is_active"]==True:
#       Use the update_or_create method of the AccountVO.objects QuerySet
        AccountVO.objects.update_or_create()
#           to update or create the AccountVO object
    else:
#   otherwise:
        AccountVO.objects.delete
#       Delete the AccountVO object with the specified email, if it exists


# Based on the reference code at
#   https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py
# infinite loop
while:
#   try
    try:
#       create the pika connection parameters
        parameters = pika.ConnectionParameters(host=rabbitmq)
#       create a blocking connection with the parameters
        connection = pika.BlockingConnection(parameters)
#       open a channel
        channel = connection.channel()
#       declare a fanout exchange named "account_info"
        channel.exchange_declare(exchange="account_info", exchange_type="fanout")
#       declare a randomly-named queue
        result = channel.queue_declare(queue="", exclusive=True)
#       get the queue name of the randomly-named queue
        queue_name = result.method.queue
#       bind the queue to the "account_info" exchange
        channel.queue_bind(exchange="account_info", queue=queue_name)
#       do a basic_consume for the queue name that calls
#           function above
        channel.basic_consume(
            queue="queue_name",
            on_message_callback=update_account_vo,
            auto_ack=True,
        )
#       tell the channel to start consuming
        print("consuming")
        channel.start_consuming()
#   except AMQPConnectionError
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
#       print that it could not connect to RabbitMQ
#       have it sleep for a couple of seconds