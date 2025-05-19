# query-to-image-search

A Python CLI tool that takes a user query, optimizes it for image search using OpenAI, and fetches relevant image URLs from Google Images via SerpAPI. The results are saved to `images.json`.

## Features

- Interactive CLI for user queries
- Uses OpenAI to optimize search phrases for images
- Fetches top 5 image URLs from Google Images using SerpAPI
- Outputs results to `images.json`

## Requirements

- Python 3.11+
- [SerpAPI](https://serpapi.com/) API key
- [OpenAI](https://platform.openai.com/) API key
- [uv](https://github.com/astral-sh/uv) for dependency management

## Installation

1. Clone the repository.
2. Install dependencies using [uv](https://github.com/astral-sh/uv):

   ```sh
   uv install
   ```


## NOTE: 
create a .env file and add the following variables
```shell
SERP_API_KEY="your_serp_api_key"
OPEN_AI_API_KEY="your_open_api_key"
```
