from discord_webhook import DiscordEmbed, DiscordWebhook
import logging
# import exception type here
import traceback
from datetime import datetime

from src.utils import get_utc_now


# Will send a notification to a discord webhook with the exception stack trace
def notify_exception(webhook_url:str, ex: Exception, service_name: str):

    stack_trace = traceback.format_exc()
    webhook = DiscordWebhook(webhook_url, rate_limit_retry=True,)

    # Make a red colored embed with "Error" as title and the message as description
    embed = DiscordEmbed(title=f'⚠ An exception occured in: {service_name} ⚠', description=f"```{stack_trace}```", color=0xff0000)
    webhook.add_embed(embed)

    # Add time to footer
    embed.set_footer(text=f"{get_utc_now()}")

    response = webhook.execute()
    logging.info(f"Exception notification sent to Discord webhook. Response: {response}")