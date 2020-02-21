import os
from random import sample

import asyncio
from aiohttp.client import ClientSession
from octomachinery.github.api.tokens import GitHubOAuthToken
from octomachinery.github.api.raw_client import RawGitHubAPI
from dotenv import load_dotenv

load_dotenv()

REACTIONS = ["+1", "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"]


async def main():
    access_token = GitHubOAuthToken(os.environ["GITHUB_TOKEN"])
    async with ClientSession() as http_session:
        gh = RawGitHubAPI(access_token, session=http_session, user_agent="drapegnik",)
        reaction = sample(REACTIONS, 1)[0]
        print(f"✨ react with {reaction}!")
        # https://github.com/Mariatta/strange-relationship/issues/243
        await gh.post(
            "/repos/mariatta/strange-relationship/issues/243/reactions",
            data={"content": reaction},
            preview_api_version="squirrel-girl",
        )


asyncio.run(main())
