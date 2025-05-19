from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from serpapi import GoogleSearch
import os
import json


class QueryFormat(BaseModel):
    query: str


class ImageDownloader:
    def __init__(self):
        # load all the environment variables from .env file
        load_dotenv()

        # create a dict to store all the envs
        self.envs = {
            "SERP_API_KEY": os.getenv("SERP_API_KEY"),
            "OPEN_AI_API_KEY": os.getenv("OPEN_AI_API_KEY"),
        }

        # validate all the envs
        for key, value in self.envs.items():
            if value is None:
                raise Exception(f"{key} can't left empty")

        # create open ai client
        self.client = OpenAI(api_key=self.envs["OPEN_AI_API_KEY"])

    def ask_user_query(self) -> str:
        user_query = input("Enter your query: ")
        return user_query

    def generate_search_query(self, user_defined_query: str) -> str:
        # validate user query
        if not user_defined_query or not user_defined_query.strip():
            raise ValueError("User query cannot be empty.")

        response = self.client.responses.parse(
            model="gpt-4o-2024-08-06",
            input=[
                {
                    "role": "system",
                    "content": "You are an image search query optimizer that transforms user inputs into effective image search phrases. Your output should be a concise, descriptive phrase of 3-7 words that will yield relevant visual results. For image searches:\n\n1. Focus on visual attributes (colors, composition, style, lighting)\n2. Include specific subject matter descriptors\n3. Add relevant artistic or photographic terminology when appropriate\n4. Avoid abstract concepts that don't translate visually\n5. Use adjectives that describe the visual appearance\n6. Omit articles, conjunctions and filler words\n7. Consider adding context terms like 'photograph', 'illustration', or specific styles",
                },
                {
                    "role": "user",
                    "content": f"Transform this query into an optimized image search phrase (3-7 descriptive words): {user_defined_query}",
                },
            ],
            text_format=QueryFormat,
        )

        parsed_query = response.output_parsed
        return parsed_query.query

    def get_images(self, query: str) -> list[str]:
        print("Searching for: ", query)
        # validate the query
        if query is None or not query.strip():
            raise ValueError("Query can't left empty")

        # define the params dict from serp api
        params = {
            "api_key": self.envs["SERP_API_KEY"],
            "engine": "google_images",
            "google_domain": "google.com",
            "q": query,
            "hl": "en",
            "gl": "us",
            "ijn": "0",
            "imgsz": "svga",
        }

        search = GoogleSearch(params)
        response = search.get_dict()
        if "images_results" not in response:
            return []

        # Get the first five images
        images = response["images_results"][:5]
        return [img.get("original") for img in images]


def main():
    image_downloader = ImageDownloader()

    # ask for user input
    user_defined_query = image_downloader.ask_user_query()

    # get the ai generated query
    generated_query = image_downloader.generate_search_query(
        user_defined_query=user_defined_query
    )

    # search in serp api
    image_res = image_downloader.get_images(generated_query)

    # print the result
    if image_res:
        with open("images.json", "w") as f:
            json.dump(image_res, f, indent=2)
        print("Image URLs saved to images.json")
    else:
        print("No images found.")


if __name__ == "__main__":
    main()
