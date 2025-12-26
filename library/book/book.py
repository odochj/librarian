from pathlib import Path
from llm.agent import Agent
from llm.config import TOC_DETECTION_PROMPT, TOC_EXTRACTION_PROMPT
from io import StringIO
from text_source import TextSource
import polars as pl

class Book:
    def __init__(self, path: Path, source: TextSource):
        self.path = path
        self.source = source
        self.title = path.stem.replace("_", " ").strip().title()
        self.contents = pl.DataFrame(
            {
                "heading": pl.Utf8, 
                "page_number": pl.Utf8
            }
        )

    def retrieve_contents(self) -> None:
        agent = Agent()

        toc_started = False
        collected_chunks = []

        for chunk in self._iter_toc_chunks(debug=True):

            if not toc_started:
                if self._is_table_of_contents(chunk):
                    toc_started = True
                    collected_chunks.append(chunk)
            else:
                if self._is_table_of_contents(chunk):
                    collected_chunks.append(chunk)
                else:
                    break  # TOC has ended → abort reading the book

        if not collected_chunks:
            return

        full_toc_text = "\n".join(collected_chunks)

        prompt = TOC_EXTRACTION_PROMPT.format(chunk=full_toc_text)
        response = agent.call(prompt)

        table = pl.read_csv(
            StringIO(response),
            has_header=False,
            sep=",",
            new_columns=["heading", "page_number"]
        )

        self.contents = table
        return None


    
    def _iter_toc_chunks(self, max_chars: int = 2000, debug: bool = False):
        buffer = []
        buffer_len = 0

        for line in self.source.iter_lines():
            line = line.strip()
            if not line:
                continue

            # Safeguard: extremely long single lines
            if len(line) > max_chars:
                if buffer:
                    chunk = "\n".join(buffer)
                    if debug:
                        print("\n--- TOC CHUNK (flush) ---\n", chunk)
                    yield chunk
                    buffer = []
                    buffer_len = 0

                if debug:
                    print("\n--- TOC CHUNK (oversize line) ---\n", line)
                yield line
                continue

            if buffer_len + len(line) > max_chars:
                chunk = "\n".join(buffer)
                if debug:
                    print("\n--- TOC CHUNK ---\n", chunk)
                yield chunk
                buffer = []
                buffer_len = 0

            buffer.append(line)
            buffer_len += len(line)

        if buffer:
            chunk = "\n".join(buffer)
            if debug:
                print("\n--- TOC CHUNK (final) ---\n", chunk)
            yield chunk
    
    def _is_table_of_contents(self, text: str) -> bool:
        agent = Agent()
        prompt = TOC_DETECTION_PROMPT.format(chunk=text)
        response = agent.call(prompt)
        return response.strip().upper() == "YES"
    