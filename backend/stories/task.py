from celery import shared_task, exceptions
from .models import StorySchedule # Use StorySchedule
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import openai
from django.conf import settings
from django.utils import timezone
import traceback

openai.api_key = settings.OPENAI_API_KEY

@shared_task(bind=True, retry_backoff=True)
def generate_and_send_story(self, schedule_id):
    try:
        schedule = StorySchedule.objects.get(id=schedule_id) # Use StorySchedule
        if schedule.story_generated:
            return

        prompt = f"Write a blog post. Preferences: {schedule.preferences}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        story = response.choices[0].message.content.strip()
        schedule.story_content = story
        schedule.story_generated = True
        schedule.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"story_user_{schedule.user.id}",
            {"type": "story.send", "story": story},
        )

    except StorySchedule.DoesNotExist: # Use StorySchedule
        print(f"Schedule with id {schedule_id} does not exist.")
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        raise self.retry(exc=e, countdown=5) #retry after 5 seconds
    except Exception as e:
        print(f"Error generating or sending story: {e}\n{traceback.format_exc()}")

@shared_task
def check_scheduled_stories():
    schedules = StorySchedule.objects.filter(scheduled_time__lte=timezone.now(), story_generated=False) # Use StorySchedule
    for schedule in schedules:
        generate_and_send_story.delay(schedule.id)