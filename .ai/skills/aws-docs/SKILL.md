---
name: aws-docs
description: Retrieve, inspect, and synthesize current official AWS documentation through the AWS Documentation MCP server. Use when Codex needs AWS service documentation, feature behavior, quotas, API/reference details, recently added AWS documentation, or a grounded answer for one AWS topic or a sequence of related AWS topics.
---

# AWS Docs

## Operating Goal

Use the AWS Documentation MCP server as the primary source for AWS documentation tasks. Produce answers grounded in `docs.aws.amazon.com`, cite the documentation URLs used, and avoid relying on memory when the user asks about current AWS behavior, limits, supported features, or recent updates.

For a series of topics, treat each topic as its own retrieval unit, then synthesize across the cited sources. Keep search intent free of PII and customer-specific identifiers.

## Workflow

1. Convert the user request into one or more AWS documentation topics.
2. Use `search_documentation` unless the user already provided a valid AWS documentation URL.
3. Prefer `read_sections` when search results include relevant `recommended_sections` or `sections`.
4. Use `read_documentation` when a full page scan is needed, paginating with `start_index` if the response is truncated.
5. Use `search_table` for large tables, service quotas, regional support, supported models, pricing-style matrices, IAM action tables, or any table that was truncated.
6. Use `recommend` after reading a page when related, similar, popular, journey, or newly released documentation may change the answer.
7. Answer with citations to the exact documentation URLs. If citing a section, include the page URL and section anchor when available from search metadata.

## MCP Operations

### `search_documentation`

Goal: Find candidate AWS documentation pages for a service, feature, API, workflow, or broad topic when the exact URL is not known.

Request contract:

```json
{
  "search_phrase": "string, required, specific AWS documentation search phrase",
  "search_intent": "string, optional, AWS-related user intent with no PII",
  "limit": "integer, optional, maximum result count",
  "product_types": "array<string> | null, optional, filters by AWS product/service",
  "guide_types": "array<string> | null, optional, filters by guide type"
}
```

Response contract:

```json
{
  "search_results": [
    {
      "rank_order": "integer",
      "url": "string",
      "title": "string",
      "context": "string | optional",
      "recommended_sections": "array<string> | optional",
      "sections": "array<string> | optional",
      "metadata": {
        "additional_urls": "array<object> | optional",
        "facets": "object | optional"
      }
    }
  ],
  "query_id": "string | optional",
  "metadata": {
    "discovered_services": "array<string> | optional",
    "related_tasks": "array<object> | optional",
    "relationships": "object | optional"
  }
}
```

Example request:

```json
{
  "search_phrase": "Amazon S3 bucket naming rules",
  "search_intent": "Find the official rules for naming Amazon S3 buckets",
  "limit": 5,
  "product_types": ["Amazon Simple Storage Service"],
  "guide_types": ["User Guide"]
}
```

Example response:

```json
{
  "search_results": [
    {
      "rank_order": 1,
      "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html",
      "title": "Bucket naming rules",
      "context": "Rules and restrictions for naming general purpose buckets.",
      "recommended_sections": ["General purpose buckets naming rules", "Best practices"],
      "sections": ["General purpose buckets naming rules", "Example general purpose bucket names", "Best practices"]
    }
  ],
  "query_id": "example-query-id"
}
```

### `read_documentation`

Goal: Fetch a full AWS documentation page as markdown when targeted sections are unavailable or a broader scan is necessary.

Request contract:

```json
{
  "url": "string, required, docs.aws.amazon.com URL ending in .html",
  "max_length": "integer, optional, maximum characters returned",
  "start_index": "integer, optional, character offset for pagination"
}
```

Response contract:

```json
{
  "content": "string, markdown documentation content",
  "metadata": {
    "url": "string | optional",
    "start_index": "integer | optional",
    "next_start_index": "integer | optional",
    "truncated": "boolean | optional"
  }
}
```

Example request:

```json
{
  "url": "https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html",
  "max_length": 12000,
  "start_index": 0
}
```

Example response:

```json
{
  "content": "# Invoking Lambda functions\n\n...",
  "metadata": {
    "url": "https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html",
    "start_index": 0,
    "next_start_index": 12000,
    "truncated": true
  }
}
```

### `read_sections`

Goal: Extract specific sections from a known AWS documentation page when only part of the page is relevant.

Request contract:

```json
{
  "url": "string, required, AWS documentation URL ending in .html",
  "section_titles": "array<string>, required, section titles to extract"
}
```

Response contract:

```json
{
  "content": "string, markdown for matching sections",
  "metadata": {
    "url": "string | optional",
    "section_titles": "array<string> | optional",
    "missing_sections": "array<string> | optional"
  }
}
```

Example request:

```json
{
  "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html",
  "section_titles": ["General purpose buckets naming rules", "Best practices"]
}
```

Example response:

```json
{
  "content": "## General purpose buckets naming rules\n\n...\n\n## Best practices\n\n...",
  "metadata": {
    "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html",
    "section_titles": ["General purpose buckets naming rules", "Best practices"]
  }
}
```

### `search_table`

Goal: Retrieve specific rows from large AWS documentation tables without loading or summarizing the full table.

Request contract:

```json
{
  "url": "string, required, AWS documentation page containing the table",
  "query": "string, required, case-insensitive row filter where all words must match",
  "section_title": "string | null, optional, exact section heading containing the table",
  "max_rows": "integer, optional, maximum matching rows per table"
}
```

Response contract:

```json
{
  "tables_searched": "integer",
  "tables_with_matches": "integer",
  "hint": "string | optional",
  "error": "string | optional, only for HTTP or transport failures",
  "results": [
    {
      "table_heading": "string | optional",
      "columns": "array<string>",
      "parent_columns": "array<string> | optional",
      "child_columns": "array<string> | optional",
      "total_rows": "integer",
      "matched_rows": "integer",
      "showing": "integer",
      "rows": "array<object>"
    }
  ]
}
```

Example request:

```json
{
  "url": "https://docs.aws.amazon.com/general/latest/gr/bedrock.html",
  "section_title": "Amazon Bedrock service quotas",
  "query": "Titan Text Embeddings V2",
  "max_rows": 10
}
```

Example response:

```json
{
  "tables_searched": 1,
  "tables_with_matches": 1,
  "results": [
    {
      "table_heading": "Amazon Bedrock service quotas",
      "columns": ["Quota", "Default", "Adjustable"],
      "total_rows": 120,
      "matched_rows": 1,
      "showing": 1,
      "rows": [
        {
          "Quota": "Titan Text Embeddings V2 requests per minute",
          "Default": "Example value",
          "Adjustable": "Yes"
        }
      ]
    }
  ]
}
```

### `recommend`

Goal: Discover related AWS documentation pages, popular pages, similar pages, user journey pages, or newly added pages for a known documentation URL.

Request contract:

```json
{
  "url": "string, required, AWS documentation page URL"
}
```

Response contract:

```json
{
  "recommendations": {
    "highly_rated": [
      {
        "url": "string",
        "title": "string",
        "context": "string | optional"
      }
    ],
    "new": "array<object>",
    "similar": "array<object>",
    "journey": "array<object>"
  }
}
```

Example request:

```json
{
  "url": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"
}
```

Example response:

```json
{
  "recommendations": {
    "highly_rated": [
      {
        "url": "https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html",
        "title": "Getting started with Lambda",
        "context": "Introductory Lambda workflow documentation."
      }
    ],
    "new": [
      {
        "url": "https://docs.aws.amazon.com/lambda/latest/dg/example-new-page.html",
        "title": "Example newly added Lambda page"
      }
    ],
    "similar": [],
    "journey": []
  }
}
```

## Error Management

Handle failures explicitly and keep progressing when possible:

- Invalid URL: If a URL is not from `docs.aws.amazon.com` or does not end in `.html` for tools that require it, search for the corresponding AWS documentation page instead of forcing the invalid URL.
- Empty search results: Rewrite the query with specific service names, API names, feature names, abbreviations, and likely guide types; then retry once or twice.
- Ambiguous service or feature: Search broader first, inspect facets or discovered services, then refine with `product_types` or `guide_types`.
- Missing section: Use exact titles from `sections` or `recommended_sections`; if still missing, fall back to `read_documentation`.
- Truncated content: Continue with `read_documentation` and `start_index` only while the missing content is needed. Stop early for very long pages once the answer is sufficiently grounded.
- Truncated table: Use `search_table` with a targeted `query` and optional exact `section_title`.
- No table matches: Report the attempted query and any returned `hint`, then broaden the query or omit `section_title`.
- MCP transport or HTTP error: Retry once if transient. If it persists, state the tool failure, what was attempted, and whether the answer is partial or blocked.
- Conflicting documentation: Prefer the most specific, current, official AWS page for the service and cite both sources when explaining the conflict.

## Answering Rules

Include citations for every factual AWS claim that depends on documentation. Distinguish clearly between directly documented facts and inferences from multiple pages. For multi-topic research, group the answer by topic and include the source URL(s) used for each group.
