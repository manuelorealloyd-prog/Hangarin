from django import template
from tasks.models import Activity

register = template.Library()


@register.simple_tag(takes_context=True)
def unread_activity(context):
    request = context["request"]

    if not request.user.is_authenticated:
        return False

    seen_id = request.session.get("activity_seen_id", 0)

    return Activity.objects.filter(
        user=request.user,
        id__gt=seen_id
    ).exists()