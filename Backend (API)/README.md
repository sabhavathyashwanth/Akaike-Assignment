---
title: Financial News Api
emoji: 👁
colorFrom: red
colorTo: indigo
sdk: docker
pinned: false
---

# Financial News API

This API fetches and analyzes news articles for publicly-traded companies, providing data for the Financial News Analyzer frontend.

## Setup

Built with Docker. Installs dependencies from `requirements.txt` and runs `api.py` on port 7860.

## Endpoints

- `GET /`: Check API status.
- `POST /api/news/fetch`: Fetch news data for a company.
- `POST /api/news/analyze`: Analyze fetched news data.
