from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
from bson.json_util import dumps

class SlackDatabaseInitializer:
    def __init__(self, db_name='slack_database', host='localhost', port=27017):
        self.client = MongoClient(host, port)
        self.db_name = db_name
        self.db = self.client[db_name]

    def create_user_collection(self):
        user_collection = self.db.create_collection('users')
        user_collection.create_index('user_id', unique=True)

        user_schema = {
            'user_id': {'type': int, 'unique': True},
            'user_name': {'type': str},
            'email': {'type': str},

        }

    def create_channel_collection(self):
        channel_collection = self.db.create_collection('channels')
        channel_collection.create_index('channel_id', unique=True)

        channel_schema = {
            'channel_id': {'type': int, 'unique': True},
            'channel_name': {'type': str},
            'members': {'type': list},

        }

    def create_workspace_collection(self):
        workspace_collection = self.db.create_collection('workspaces')
        workspace_collection.create_index('workspace_id', unique=True)

        workspace_schema = {
            'workspace_id': {'type': int, 'unique': True},
            'workspace_name': {'type': str},
            'channels': {'type': list},
            'users': {'type': list},
        }

    def create_messages_collection(self):
        messages_collection = self.db.create_collection('messages')
        messages_collection.create_index('message_id', unique=True)

        messages_schema = {
            'message_id': {'type': int, 'unique': True},
            'message_type': {'type': str},
            'message_content': {'type': str},
            'sender_id': {'type': int},
            'channel_id': {'type': int},
            'message_sent_time': {'type': int},
            'reply_count': {'type': int},
            'reply_users_count': {'type': int},
            'reply_users': {'type': list},
            'time_thread_start': {'type': int},
            'time_thread_end': {'type': int},

        }

    def create_threads_collection(self):
        threads_collection = self.db.create_collection('threads')
        threads_collection.create_index('thread_id', unique=True)

        threads_schema = {
            'thread_id': {'type': int, 'unique': True},
            'messages': {'type': list},
            'participants': {'type': list},

        }

    def create_denormalized_collection(self):
        denormalized_collection = self.db.create_collection('denormalized_data')

        denormalized_schema = {
            'message_type': {'type': str},
            'message_content': {'type': str},
            'sender_name': {'type': str},
            'message_sent_time': {'type': int},
            'message_dist_type': {'type': str},
            'time_thread_start': {'type': int},
            'replay_count': {'type': int},
            'reply_users_count': {'type': int},
            'reply_users': {'type': list},
            'time_thread_end': {'type': int},
            'channel': {'type': str},
        }
        denormalized_collection.create_index('message_id', unique=True)

    def initialize_database(self):
        self.create_user_collection()
        self.create_channel_collection()
        self.create_workspace_collection()
        self.create_messages_collection()
        self.create_threads_collection()
        self.create_denormalized_collection()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/users':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()


            initializer = SlackDatabaseInitializer()
            initializer.initialize_database()

            client = MongoClient('mongodb://localhost:27017/')
            db = client['slack_database']

        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':

    initializer = SlackDatabaseInitializer()
    initializer.initialize_database()

    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, RequestHandler)

    print('Starting server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print('Server stopped.')