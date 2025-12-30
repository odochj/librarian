# librarian
An interactive catalogue for non-fiction literature


*Librarian* addresses two problems I've had recently regarding personal development:
1. I am much better at buying books than reading them
2. AI learning assistants tend to focus on summarising material, often missing nuance

Solution:
1. Use a local LLM organise my books into the subjects they cover based on their table of contents **only**
2. Communicate my learning goals to the same LLM, and map those goals to the subjects I've catalogued
3. Return a reading list with the exact pages needed from each book I own (whilst also highlighting any subjects that are not covered)

```
src/
└── librarian/
    ├── database/
    │   ├── library.py
    │   └── schema.sql
    ├── entities/
    │   ├── book.py
    │   └── subject.py
    ├── inference/
    │   ├── book.py
    │   ├── subject.py
    │   └── user.py
    ├── llm/
    │   ├── agent.py
    │   ├── config.py
    ├── sources/
    │   ├── image_source.py
    │   ├── pdf_source.py
    │   └── text_source.py
    ├─── librarian.py
    ├──scripts/
    │   ├── create_curriculum.py
    │   └── populate_library.py
    └──tests/
```