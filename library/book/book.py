from pathlib import Path
from llm.agent import Agent
from llm.config import TOC_DETECTION_PROMPT, TOC_EXTRACTION_PROMPT
from io import StringIO
from text_source import TextSource
import polars as pl

class Book:
    def __init__(self, path: Path):
        self.path = path
        self.source = TextSource()
        self.title = path.stem.replace("_", " ").strip().title()
        self.contents = pl.DataFrame(
            {
                "heading": pl.Utf8, 
                "page_number": pl.Utf8
            }
        )

    def retrieve_contents(self) -> None:
        """
        Chunk through the book until the table of contents is found
        Return a polars DataFrame of page numbers (as strings) and 
        headings
        """
        agent = Agent()
        for chunk in self.source.iter_chunks():
            if self._is_table_of_contents(chunk):
                prompt = TOC_EXTRACTION_PROMPT.format(chunk=chunk)
                response = agent.call(prompt)
                table_of_contents = pl.read_csv(
                    StringIO(response),
                    has_header=False,
                    sep=",",
                    new_columns=["heading", "page_number"]
                )
                self.contents = pl.concat(
                    [self.contents, table_of_contents],
                    how="vertical"
                )
                return None

        
        return None
    
    def _is_table_of_contents(self, text: str) -> bool:
        agent = Agent()
        prompt = TOC_DETECTION_PROMPT.format(chunk=text)
        response = agent.call(prompt)
        return response.strip().upper() == "YES"
    