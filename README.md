04/30/2015

Email Service
=============

A Minimalist email service that supports fail over using two different email service providers.  
If one service goes down, the other is used as a backup.  If both services are down, the email  
is re-queued using AMQP. The HTTP server is implemented in Tornado and accepts POST requests that  
include the 'to', 'subject', and 'text' fields.  Tornado queues the email request to AMQP via  
celery and is backed by Redis.  A celery worker handles the actual email requests and re-queues  
if necessary.

`
POST /send HTTP/1.1
Accept: application/json
Content-Length: 76
Content-Type: application/json; charset=utf-8

{
  "to": "brian.refsdal@gmail.com",
  "subject": "Test Email",
  "text": "Hello World"
}
`