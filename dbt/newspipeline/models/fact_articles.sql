-- models/fact_articles.sql
SELECT
    url AS article_id,
    title,
    published_at,
    DATE(published_at) AS date_id,
    source_id,
    keyword,
    author,
    description,
    content,
    language,
    word_count,
    sentiment_score
FROM
    {{ ref('raw_landing') }}
