# librarian
An interactive catalogue for non-fiction literature

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