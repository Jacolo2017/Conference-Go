import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()

while True:
    try:
        def process_approvals(ch, method, properties, body):
            data = json.loads(body)
            email = data["presenter_email"]
            title = data["title"]
            name = data["presenter_name"]

            send_mail(
                "Your presentation has been approved",
                f"{name}, we are happy to tell you that your presentation {title} has been accepted",
                "admin@conference.go",
                [email],
                fail_silently=False,
            )

        def process_rejection(ch, method, properties, body):
            data = json.loads(body)
            email = data["presenter_email"]
            title = data["title"]
            name = data["presenter_name"]

            send_mail(
                "Your presentation has been rejected",
                f"{name}, were sad to tell you that your presentation {title} has been rejected",
                "admin@conference.go"
                [email],
                fail_safely=False,
            )


        # def process_message(ch, method, properties, body):
        #     print("  Received %r" % body)
            # send_mail(
            #     'Subject',
            #     'Here is the message.',
            #     'from@example.com',
            #     ['to@example.com'],
            #     fail_silently=False,
            # ))
        parameters = pika.ConnectionParameters(host='rabbitmq')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='presentation_approvals')
        channel.queue_declare(queue='presentation_rejections')
        channel.basic_consume(
            queue='presentation_approvals',
            on_message_callback=process_approvals,
            auto_ack=True,
        )
        channel.basic_consume(
            queue='presentation_rejections',
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        print("we are consuming")
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
