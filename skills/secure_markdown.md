# Secure Markdown Rendering

## Purpose
Prevent XSS and other injection attacks when rendering user-provided Markdown content in blog posts.

## When to Use
- When displaying blog post content in templates (`posts/detail.html`, `posts/list.html`, etc.).
- When adding new fields that support Markdown.

## Rules
1. **Sanitization:** All content rendered from Markdown MUST be passed through the `markdown` Jinja2 filter.
2. **Filter Implementation:** Ensure the filter in `app/web/routes.py` uses `bleach.clean` with a strict `CSSSanitizer`.
3. **Allowed Tags:** Only allow safe HTML tags (p, h1-h6, blockquote, code, pre, img, etc.).

## Constraints
- Never use the `| safe` filter on raw database content without prior sanitization.
- Always sanitize the `style` attribute using `CSSSanitizer` if styles are allowed.

## Expected Output
Code changes in templates that use `{{ content | markdown | safe }}` and updates to the `markdown_filter` if new tags or attributes are needed.
