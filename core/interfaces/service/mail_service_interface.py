import abc
from typing import List, TypedDict, Union


class MailMailAttribute(TypedDict):
    sender_address: str
    sender_name: str
    password: str
    recipient: Union[List[str], str]
    subject: str
    html_body: str
    text_body: str


class MailServiceInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "send"))
            and callable(subclass.send)
            and hasattr(subclass, "client")
        )

    @property
    def client(self):
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, email_attribute: MailMailAttribute):
        raise NotImplementedError
