import redis


# Initialize Redis connection
# redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)


class RedisClient:
    def __init__(self, host="localhost", port=6379, decode_responses=True):
        self.host = host
        self.port = port
        self.decode_responses = decode_responses
        self.client = None

    def connect(self):
        """Establishes the connection to Redis."""
        try:
            self.client = redis.StrictRedis(
                host=self.host, port=self.port, decode_responses=self.decode_responses
            )
            self.client.ping()  # Test connection
            print("Connected to Redis")
        except redis.ConnectionError:
            raise RuntimeError("Failed to connect to Redis")

    def get_client(self):
        """Returns the Redis client instance."""
        if self.client is None:
            self.connect()
        return self.client
