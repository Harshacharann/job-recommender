from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_naukri_jobs

# Initialize FastMCP with the job fetching functions
mcp = FastMCP("Job Recommender", "Job Fetching API")


@mcp.tool()
async def fetchnaukri(listofkey):
    return fetch_naukri_jobs(listofkey, rows=60)


if __name__ == "__main__":
    mcp.run(transport="stdio")
