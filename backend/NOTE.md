## Architecture
Main picture:
1. API layer: talk to the outside world
2. Domain layer: product logic
3. Infrastruction layer: how the underlying is done

```
api/ = “HTTP translators”
domain/ = “what the app means”
infrastructure/ = “how the app does it”
workers/ = “slow tasks off the request thread”
```

Directories:
`app/api/`
- Handle request: convert HTTP requests -> calls to domain 
- Handle outputs: convert domain outputs -> HTTP responses
```
api/router.py
api/v1/
api/v1/media.py
api/v1/entries.py
api/v1/timeline.py
```

<br>

`app/domain/`
`app/domain/entries`
It does not need to know the underlying infra shape like S3 or Whisper or Redis.
```
entries/models.py: entry shape for SQLAlchemy(which is not a real db, an abstraction layer to connect to db)
entries/schemas.py: keep api stable even if the db schema change. define what accepts as input and what returns as output
entries/repo.py: db query for basic create, fetch, update status
entries/timeline.py: product logic to compute daily emotional aggregation result
```

`app/domain/media`
Everything about attached media
```
media/models.py: db shape for media 
media/repo.py: db query related to media
```

```
Request (HTTP POST)
   │
   ▼
[API Layer] (api/v1/entries.py)
   │  • Receives JSON
   │  • Validates it matches EntryCreate schema
   │  • Calls service.create_entry()
   │
   ▼
[Service Layer] (domain/entries/service.py)
   │  • "Brain" logic: Is user active? Is text valid?
   │  • Calls repo.save()
   │  • Triggers background job for sentiment analysis
   │
   ▼
[Repo Layer] (domain/entries/repo.py)
   │  • "Librarian" logic: database.add(entry), database.commit()
   │
   ▼
[Database] (infrastructure/db)
   • Saves row to Postgres
```


`app/domain/entries`
Main logic:
```
Creation -> Asynchronous Analysis -> Aggregation
```

`models.py`
```
The files defines what an Entry looks likes in Postgres db
1. input(entry_text) and output(valence, arousal, emotions) are stored.
2. status represent the async state machine
3. ML datatype:
   - valence/ arousal: floats for graphing mood on X/Y axes
   - emotions: A JSON blob {"top":[{"label": "joy", "score": 0.9}]}
```