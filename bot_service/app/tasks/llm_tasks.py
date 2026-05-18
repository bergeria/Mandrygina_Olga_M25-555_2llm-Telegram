import asyncio

from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient


@celery_app.task(name="llm_request")
def llm_request(prompt: str) -> str:
    return asyncio.run(run_llm_request(prompt))


async def run_llm_request(prompt: str) -> str:
    client = OpenRouterClient()

    response = await client.ask(prompt)

    return response
