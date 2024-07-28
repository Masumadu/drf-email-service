import enum


class MailDeliveryStatusEnum(enum.Enum):
    sent_to_provider = "sent_to_provider"
    not_sent_to_provider = "not_sent_to_provider"
