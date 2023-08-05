import pika, requests, threading, json, time
from logzero import logger


class AutoSolve:
    SUCCESS = "info"
    WARNING = "warning"
    ERROR = "error"
    STATUS = "status"

    EXCHANGE = "exchanges.autosolve"
    SENDER = "token.request"
    RECEIVER = "token.response"
    HEARTBEAT = 10

    def __init__(self, access_token, api_key, client_key, receiver_function, debug):
        self.access_token = access_token
        self.api_key = api_key
        self.client_key = client_key
        self.receiver_function = receiver_function
        self.username = ""
        self.vhost = ""
        self.routing_key = ""
        self.queue_name = self.api_key.replace("-", "")
        self.connection = None
        self.channel = None
        self.consumer_thread = None
        self.debug = debug
        self.ready = False
        self.connected = False
        self.message_backlog = []
        self.start_connection_process()

    def initialized(self):
        while True:
            time.sleep(.5)
            if self.ready:
                break
        return True

    def start_connection_process(self):
        if self.check_input_values():
            self.create_routing_key()
            self.establish_rabbit_session()

    def establish_rabbit_session(self):
        self.consumer_thread = threading.Thread(target=self.begin_connection)
        valid = self.validate_connection()
        if valid == 400:
            self.log(self.INVALID_CLIENT_KEY, self.ERROR)
            raise AuthException(self.INVALID_CLIENT_KEY)
        if valid == 401:
            self.log(self.INVALID_API_KEY_OR_ACCESS_TOKEN, self.ERROR)
            raise AuthException(self.INVALID_API_KEY_OR_ACCESS_TOKEN)
        else:
            self.log("Validation complete", self.SUCCESS)
            self.username = self.access_token.split("-")[0]
            self.vhost = self.username
            self.consumer_thread.start()

    def begin_connection(self):
        self.log("Beginning connection establishment", self.STATUS)

        credentials = pika.PlainCredentials(self.username, self.access_token)
        parameters = pika.ConnectionParameters(host='rabbit.autosolve.io',
                                               port=5672,
                                               virtual_host=self.vhost,
                                               credentials=credentials,
                                               connection_attempts=50,
                                               blocked_connection_timeout=60,
                                               heartbeat=self.HEARTBEAT)
        try:
            self.connection = pika.BlockingConnection(parameters)
            self.log("Connection established", self.SUCCESS)

            self.log("Creating channel", self.STATUS)
            self.channel = self.connection.channel()
            self.channel.confirm_delivery()
            self.log("Channel created", self.SUCCESS)

            self.log("Declaring exchange", self.STATUS)
            self.channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='direct', durable=True)
            self.channel.queue_declare(self.queue_name, durable=True, auto_delete=False)

            self.log("Queue " + self.queue_name + " declared", self.SUCCESS)

            self.log("Binding queue to exchange", self.STATUS)
            self.channel.queue_bind(queue=self.queue_name, exchange=self.EXCHANGE, routing_key=self.routing_key)
            self.log("Queue binded to exchange " + self.EXCHANGE, self.SUCCESS)

            self.channel.basic_consume(queue=self.queue_name, auto_ack=True, on_message_callback=self.on_message)
            self.log("Beginning message consumption", self.SUCCESS)
            self.ready = True
            self.connected = True
            self.channel.start_consuming()

        except pika.exceptions.AMQPConnectionError or pika.exceptions.ConnectionClosedByBroker:
            self.log("Error with RabbitMQ connection, attempting to re-establish", self.WARNING)
            self.handle_connection_error()

    def close_connection(self):
        self.connection.close()

    def on_message(self, channel, method_frame, header_frame, body):
        json_string = "".join(chr(x) for x in body)
        json_object = json.loads(json_string)
        self.log("Message Received: " + json_string, self.SUCCESS)
        self.receiver_function(json_object)

    def handle_connection_error(self):
        self.connected = False
        while True:
            try:
                self.begin_connection()
            except pika.exceptions.ConnectionClosedByBroker:
                break
            except pika.exceptions.AMQPConnectionError:
                continue

        if self.connected:
            self.log("Connection attempt successful, sending any unsent messages", self.SUCCESS)
            self.attempt_message_backlog_send()
        else:
            self.log("Connection attempts unsuccessful", self.ERROR)

    def send(self, message):
        message_string = json.dumps(message)
        byte_string = message_string.encode()
        return self.channel.basic_publish(exchange=self.EXCHANGE,
                                          routing_key=self.SENDER,
                                          body=byte_string)

    def send_token(self, message):
        self.log("Sending message for task: " + message['taskId'], self.STATUS)
        try:
            send_result = self.send(message)
            if send_result is None:
                self.log("Message with TaskId: " + message['taskId'] + " sent successfully", self.SUCCESS)
        except Exception as e:
            self.log(e, self.WARNING)
            self.resend(message)

    def resend(self, message):
        time.sleep(5)
        result = self.send(message)
        if result is None:
            self.log("Resend attempt successful", self.SUCCESS)
        else:
            self.log("Attempt to resend after wait unsuccessful. Pushing message to backlog", self.WARNING)
            self.add_message_to_backlog(message)

    def add_message_to_backlog(self, message):
        self.message_backlog.append(message)

    def attempt_message_backlog_send(self):
        self.log("Sending messages from backlog", self.STATUS)
        message_cache = self.message_backlog
        for message in message_cache:
            result = self.send(message)
            if result is None:
                self.message_backlog.remove(message)

    ## VALIDATION FUNCTIONS ##

    def check_input_values(self):
        if self.validate_inputs():
            return True
        else:
            self.log(self.INPUT_VALUE_ERROR, self.ERROR)
            raise InputValueException(self.INPUT_VALUE_ERROR)

    def validate_inputs(self):
        valid_access_token = self.validate_access_token()
        valid_client_key = self.client_key is not None
        valid_api_key = self.api_key is not None

        return valid_access_token and valid_client_key and valid_api_key

    def validate_access_token(self):
        if self.access_token is None:
            return False

        access_token_split = self.access_token.split("-")
        username_valid = access_token_split[0].isdigit()

        if username_valid is not True:
            return False

        return True

    def validate_connection(self):
        self.log("Validating input values with AutoSolve API", self.STATUS)
        url = "https://dashboard.autosolve.io/rest/" + self.access_token + "/verify/" + self.api_key + "?clientId=" + self.client_key
        response = requests.get(url)
        return response.status_code

    def create_routing_key(self):
        self.routing_key = self.api_key.replace("-", "") + "." + self.RECEIVER

    def log(self, message, type):
        if type == self.ERROR:
            logger.error(message)
        if type == self.WARNING:
            logger.warning(message)
        if self.debug:
            if type == self.STATUS:
                logger.debug(message)
            if type == self.SUCCESS:
                logger.info(message)

    INVALID_CLIENT_KEY = "Invalid Client Key"
    INVALID_API_KEY_OR_ACCESS_TOKEN = "Invalid API or Access Key"
    INPUT_VALUE_ERROR = "Input value for access_token is invalid or client_key/api_key are not set"


class AuthException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'AuthException: {}'.format(self.value)


class InputValueException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'InputValueException: {}'.format(self.value)
