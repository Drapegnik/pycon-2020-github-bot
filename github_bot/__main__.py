from datetime import datetime

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
    url = comment["url"]
    await github_api.post(
        f"{url}/reactions",
        data={"content": "confused"},
        preview_api_version="squirrel-girl",
    )


@process_event_actions("pull_request", {"opened", "edited"})
@process_webhook_payload
async def on_pr_check_wip(*, pull_request, repository, **_kw):
    github_api = RUNTIME_CONTEXT.app_installation_client
    check_run_name = "WIP state"

    pr_head_sha = pull_request["head"]["sha"]
    repo_api_url = repository["url"]

    check_runs_base_uri = f"{repo_api_url}/check-runs"

    resp = await github_api.post(
        check_runs_base_uri,
        preview_api_version="antiope",
        data={
            "name": check_run_name,
            "head_sha": pr_head_sha,
            "status": "queued",
            "started_at": f"{datetime.utcnow().isoformat()}Z",
        },
    )

    check_runs_updates_uri = f'{check_runs_base_uri}/{resp["id"]:d}'

    resp = await github_api.patch(
        check_runs_updates_uri,
        preview_api_version="antiope",
        data={"name": check_run_name, "status": "in_progress",},
    )

    pr_title = pull_request["title"].lower()
    wip_markers = (
        "wip",
        "🚧",
        "dnm",
        "work in progress",
        "work-in-progress",
        "do not merge",
        "do-not-merge",
        "draft",
    )

    is_wip_pr = any(m in pr_title for m in wip_markers)

    await github_api.patch(
        check_runs_updates_uri,
        preview_api_version="antiope",
        data={
            "name": check_run_name,
            "status": "completed",
            "conclusion": "success" if not is_wip_pr else "neutral",
            "completed_at": f"{datetime.utcnow().isoformat()}Z",
            "output": {
                "title": "🤖 This PR is not Work-in-progress: Good to go",
                "text": "Debug info:\n"
                f"is_wip_pr={is_wip_pr!s}\n"
                f"pr_title={pr_title!s}\n"
                f"wip_markers={wip_markers!r}",
                "summary": "This change is ready to be reviewed."
                "\n\n"
                "![Go ahead and review it!]("
                "https://farm1.staticflickr.com"
                "/173/400428874_e087aa720d_b.jpg)",
            }
            if not is_wip_pr
            else {
                "title": "🤖 This PR is Work-in-progress: " "It is incomplete",
                "text": "Debug info:\n"
                f"is_wip_pr={is_wip_pr!s}\n"
                f"pr_title={pr_title!s}\n"
                f"wip_markers={wip_markers!r}",
                "summary": "🚧 Please do not merge this PR "
                "as it is still under construction."
                "\n\n"
                "![Under constuction tape]("
                "https://cdn.pixabay.com"
                "/photo/2012/04/14/14/59"
                "/border-34209_960_720.png)\n"
                "![Homer's on the job]("
                "https://farm3.staticflickr.com"
                "/2150/2101058680_64fa63971e.jpg)",
            },
        },
    )


if __name__ == "__main__":
    run_app(
        name="pycon-2020-github-bot",
        version="1.0.0",
        url="https://github.com/apps/octomachinery",
    )
