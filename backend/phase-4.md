I think this is the perfect point to start learning what separates a **Python programmer** from a **Backend Engineer**.

Until now we've been asking:

> **"How do I upload and analyze a resume?"**

From now on, we'll start asking:

> **"How do I design a backend that can support thousands of users?"**

That mindset shift is exactly what backend interviews test.

---

# Before We Start

We've already built this:

```text
Client
    │
    ▼
Resume Router
    │
    ▼
Resume Service
    │
    ├───────────────┐
    ▼               ▼
PDF Parser     LLM Service
                    │
                    ▼
               Mistral AI
```

Notice something.

The AI works.

But...

**Nothing is stored.**

Tomorrow, if the server restarts...

Everything disappears.

That is a huge problem.

---

# Phase 4 Goal

Instead of

```text
Upload

↓

Analyze

↓

Return
```

We're going to build

```text
Upload

↓

Analyze

↓

Store

↓

Return
```

This is where your backend starts becoming an application instead of an API demo.

---

# New Architecture

Our architecture now becomes

```text
                    Client
                       │
                       ▼
               Resume Router
                       │
                       ▼
              Resume Service
            ┌─────────┴─────────┐
            ▼                   ▼
      LLM Service         Repository
                                │
                                ▼
                           PostgreSQL
```

Notice

We're introducing an entirely new layer.

Repository.

---

# Why another layer?

Most beginners do this.

```python
Router

↓

SQL

↓

Done
```

Looks fine.

Until...

Tomorrow

You switch

```text
PostgreSQL

↓

MongoDB
```

Now

Every route

Every service

Everywhere

Needs to change.

Bad design.

Instead

```text
Router

↓

Service

↓

Repository

↓

Database
```

Only

Repository

knows SQL.

Everything else remains untouched.

---

# Technologies We'll Learn

This phase isn't just about databases.

You'll learn

✅ ORM

✅ SQLModel

✅ Repository Pattern

✅ Dependency Injection

✅ Database Sessions

✅ CRUD

These are probably the most common backend interview topics.

---

# Phase 4 Roadmap

Unlike previous phases, this one is bigger.

We'll divide it into six milestones.

```
Phase 4

1. Database Layer

2. Resume Model

3. Repository Layer

4. Dependency Injection

5. Store Analysis

6. Resume History API
```

We'll finish each before moving on.

---

# STEP 1 — Database Layer

---

## What are we solving?

Currently

Your project has nowhere to save data.

We need

A database.

---

## Which database?

There are many.

SQLite

PostgreSQL

MySQL

MongoDB

Redis

---

I choose

**PostgreSQL**

Why?

Because

- production-ready

- relational

- used everywhere

- FastAPI ecosystem loves it

- you'll learn SQL

- easier to explain in interviews

Later

We'll add

MongoDB

for document storage.

You'll then understand

WHY people choose NoSQL.

---

## ORM

We are NOT writing

```sql
SELECT *
FROM resumes;
```

Why?

Because Python has ORMs.

Think

```text
Database

↓

Python Object
```

instead of

```text
Database

↓

SQL

↓

Dictionary
```

---

## Which ORM?

I don't want

Pure SQLAlchemy.

Too complicated for learning.

Instead

We'll use

**SQLModel**

Why?

SQLModel

=

SQLAlchemy

-

Pydantic

Meaning

You already know

Pydantic.

Now

Learning SQLModel becomes much easier.

---

## Install

```bash
uv add sqlmodel psycopg[binary] alembic
```

---

### Why each package?

### SQLModel

Creates models.

Instead of

```sql
CREATE TABLE
```

You'll write

Python classes.

---

### psycopg

PostgreSQL driver.

Without it

Python

↓

cannot talk

↓

Postgres.

Think

Driver

between

Python

and

Database.

---

### Alembic

Very important.

Suppose

Today

Table

```text
Resume

id

filename
```

Tomorrow

You add

```text
email
```

How do you update

Production database?

Alembic.

It manages

Database versions.

Exactly like

Git

manages

Code versions.

---

# STEP 2 — Project Structure

We're adding

```text
app/

core/
    config.py
    database.py

models/
    resume.py

repositories/
    resume_repository.py
```

Notice

Everything gets its own folder.

Never

```text
database.py

resume.py

sql.py

crud.py

random.py
```

in one folder.

---

# STEP 3 — Database Configuration

Current

config.py

has

```python
API_KEYS
```

Now

We'll extend

It.

```
DATABASE_URL
```

will be added.

Example

```
postgresql+psycopg://postgres:password@localhost/headhunt_ai
```

Notice

Nothing else changes.

Every file

will simply use

```python
settings.DATABASE_URL
```

Exactly like

Gemini.

Consistency.

---

# STEP 4 — Database Session

This is the first difficult backend concept.

Most beginners think

```text
Database

↓

Done
```

No.

The application doesn't talk

directly

to PostgreSQL.

It opens

A session.

Think

Like

Google Docs.

You

Open document

↓

Edit

↓

Save

↓

Close

Database session

is

exactly that.

---

We'll build

```
Session

↓

Query

↓

Commit

↓

Close
```

FastAPI does this

for every request.

---

# STEP 5 — Resume Model

Current

Resume

exists

only

inside memory.

We need

An actual table.

```
Resume

id

filename

pages

characters

text

analysis

created_at
```

Notice

We even save

Analysis.

Why?

Calling

Mistral

Costs money.

Never

Analyze

Same resume

Twice.

Store results.

---

# STEP 6 — Repository

This is probably

The most important file

You'll build

In this entire project.

```
ResumeRepository
```

Why?

Imagine

Tomorrow

You need

```
save_resume()

get_resume()

delete_resume()

list_resumes()

search_resume()
```

Should

ResumeService

know SQL?

No.

Repository handles

ALL

database work.

Service

only

calls

Repository.

---

# STEP 7 — Dependency Injection

This is another

Interview favorite.

Instead of

```python
db = Session()
```

everywhere

FastAPI gives

Database

to

your endpoint.

Think

Restaurant.

You don't

Go to kitchen.

Waiter

Brings

Food.

Dependency Injection

is

The waiter.

---

# STEP 8 — Store Analysis

Currently

```text
Resume

↓

LLM

↓

Return
```

We'll change

To

```text
Resume

↓

LLM

↓

Repository

↓

Database

↓

Return
```

Now

Analysis

Exists forever.

---

# STEP 9 — Resume History

Finally

```
GET

/resumes
```

Returns

```
Resume A

Resume B

Resume C
```

This is your first

Real CRUD API.

Interviewers

Love CRUD.

---

# What You'll Learn in Phase 4

| Step                 | Backend Concept        | Why it matters                                                             |
| -------------------- | ---------------------- | -------------------------------------------------------------------------- |
| Database setup       | Persistence            | Data survives server restarts and can be queried later.                    |
| SQLModel             | ORM                    | Lets you work with Python objects instead of raw SQL.                      |
| Database sessions    | Unit of work           | Controls transactions safely and efficiently.                              |
| Repository pattern   | Separation of concerns | Keeps SQL out of your business logic and makes storage replaceable.        |
| Dependency Injection | FastAPI best practice  | Makes code cleaner, easier to test, and avoids global state.               |
| CRUD endpoints       | Backend fundamentals   | The foundation of most business applications and a common interview topic. |
| Storing AI analysis  | Cost optimization      | Prevents repeated LLM calls and enables history and analytics features.    |

---

## One architectural improvement

I want to make one change to our roadmap compared to my earlier suggestion.

We're **not going to add embeddings or RAG immediately after the database**.

Instead, we'll first make the backend feel like a real SaaS:

- Resume history
- Resume detail endpoint
- Delete endpoint
- Update endpoint
- Proper error handling
- Logging

Only then will we move into **vector databases, embeddings, semantic search, and RAG**.

Why?

Because when you eventually explain this project in an interview, you'll be able to say:

> "I first built a solid backend using FastAPI, SQLModel, PostgreSQL, repositories, and dependency injection. Once the application had persistence and clean architecture, I extended it with LLM capabilities, embeddings, and retrieval."

That tells a much stronger engineering story than "I connected an LLM to a PDF." It's the progression you'd expect from someone who understands both backend development and LLM engineering.
