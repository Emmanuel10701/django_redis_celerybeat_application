from celery import shared_task, exceptions
from .models import StorySchedule  # Use StorySchedule
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import openai
from django.conf import settings
from django.utils import timezone
import traceback
import logging

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY

@shared_task(bind=True, retry_backoff=True)
def generate_and_send_story(self, schedule_id):
    logger.info(f"Starting task to generate and send story for schedule ID: {schedule_id}")
    try:
        schedule = StorySchedule.objects.get(id=schedule_id)  # Use StorySchedule
        logger.debug(f"Retrieved schedule: {schedule}")
        if schedule.story_generated:
            logger.info(f"Story already generated for schedule ID: {schedule_id}. Skipping.")
            return

        prompt = f"Write a blog post. Preferences: {schedule.preferences}"
        logger.info(f"Sending prompt to OpenAI for schedule ID {schedule_id}: {prompt}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        story = response.choices[0].message.content.strip()
        logger.info(f"Received generated story for schedule ID {schedule_id}: {story}")
        schedule.story_content = story
        schedule.story_generated = True
        schedule.save()
        logger.info(f"Story saved for schedule ID: {schedule_id}")

        channel_layer = get_channel_layer()
        group_name = f"story_user_{schedule.user.id}"
        message = {"type": "story.send", "story": story}
        logger.info(f"Sending story to group '{group_name}' for user ID {schedule.user.id}: {message}")
        async_to_sync(channel_layer.group_send)(
            group_name,
            message,
        )
        logger.info(f"Story sent to group '{group_name}' for user ID {schedule.user.id}")

    except StorySchedule.DoesNotExist:  # Use StorySchedule
        error_message = f"Schedule with id {schedule_id} does not exist."
        logger.error(error_message)
        print(error_message)
    except openai.error.OpenAIError as e:
        error_message = f"OpenAI API error for schedule ID {schedule_id}: {e}"
        logger.error(error_message)
        print(error_message)
        raise self.retry(exc=e, countdown=5)  # retry after 5 seconds
    except Exception as e:
        error_message = f"Error generating or sending story for schedule ID {schedule_id}: {e}\n{traceback.format_exc()}"
        logger.error(error_message)
        print(error_message)

@shared_task
def check_scheduled_stories():
    logger.info("Checking for scheduled stories to process...")
    schedules = StorySchedule.objects.filter(scheduled_time__lte=timezone.now(), story_generated=False)  # Use StorySchedule
    logger.info(f"Found {schedules.count()} scheduled stories to process.")
    for schedule in schedules:
        logger.info(f"Dispatching generate_and_send_story task for schedule ID: {schedule.id}")
        generate_and_send_story.delay(schedule.id)
    logger.info("Finished checking for scheduled stories.")