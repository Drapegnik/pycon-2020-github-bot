from octomachinery.app.server.runner import run as run_app
from octomachinery.routing import process_event_actions
from octomachinery.routing.decorators import process_webhook_payload
from octomachinery.runtime.context import RUNTIME_CONTEXT


@process_event_actions("issues", {"opened"})
@process_webhook_payload
async def on_issue_opened(*, issue, **_kw):
    github_api = RUNTIME_CONTEXT.app_installation_client
    url = issue["comments_url"]
    author = issue["user"]["login"]
    message = (
        f"Thanks for the report @{author}! " "I will look into it ASAP! (I'm a bot 🤖)."
    )
    await github_api.post(url, data={"body": message})


@process_event_actions("pull_request", {"closed"})
@process_webhook_payload
async def on_pr_closed(*, pull_request, **_kw):
    github_api = RUNTIME_CONTEXT.app_installation_client
    url = pull_request["comments_url"]
    author = pull_request["user"]["login"]
    message = f"Thanks for your contribution @{author}! 🦄"
    await github_api.post(url, data={"body": message})


@process_event_actions("issue_comment", {"created"})
@process_webhook_payload
async def on_comment_created(*, comment, **_kw):
    github_api = RUNTIME_CONTEXT.app_installation_client
    url = comment["comments_url"]
    await github_api.post(
        f"{url}/reactions",
        data={"content": "confused"},
        preview_api_version="squirrel-girl",
    )


if __name__ == "__main__":
    run_app(
        name="pycon-2020-github-bot",
        version="1.0.0",
        url="https://github.com/apps/octomachinery",
    )
