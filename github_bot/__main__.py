from octomachinery.app.server.runner import run as run_app
from octomachinery.routing import process_event_actions
from octomachinery.routing.decorators import process_webhook_payload
from octomachinery.runtime.context import RUNTIME_CONTEXT


@process_event_actions("issues", {"opened"})
@process_webhook_payload
async def on_issue_opened(*, issue, **_kw):
    """Whenever an issue is opened, greet the author and say thanks."""
    github_api = RUNTIME_CONTEXT.app_installation_client
    url = issue["comments_url"]
    author = issue["user"]["login"]
    message = (
        f"Thanks for the report @{author}! " "I will look into it ASAP! (I'm a bot 🤖)."
    )
    await github_api.post(url, data={"body": message})


if __name__ == "__main__":
    # https://github-bots.herokuapp.com
    run_app(
        name="pycon-2020-github-bot",
        version="1.0.0",
        url="https://github.com/apps/octomachinery",
    )
