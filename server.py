/* Febonachi number*/
#include <unistd.h> 
#include <stdio.h> 
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>

void fibonachi(int length){
	printf("arg is: %d\n", length);
	int status;
	
	if(fork() == 0){
		printf("Second Child PID is: %d\n", getpid());
		int number = 0;
		int next_number = 1;
		for(int i = 0; i<length; i++){
			printf("%d,\t", number);
			int temp = next_number;
			next_number += number;
			number = temp; 
		}
		printf("\n");
	}
	else{
		printf("Second Parent PID is: %d\n", getpid());
		wait(&status);
		printf("Second Child terminated: %d\n", status);
		
	}
}

void main(int argc, char *argv[]){
	//take input from user.
	int number = atoi(argv[1]);
	fibonachi(number);
}

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()