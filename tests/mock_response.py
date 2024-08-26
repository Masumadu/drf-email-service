from amqp import exceptions as amqp_exc


class MockSideEffects:
    status_code = 200
    json = None

    def celery_exc(self, *args, **kwargs):
        raise amqp_exc.AMQPError
