import markdown2
import bleach

def markdown_filter(text):
    html = markdown2.markdown(text, extras=["fenced-code-blocks", "tables"])
    allowed_tags = bleach.ALLOWED_TAGS | {
        'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'pre', 'code', 'span', 'div', 'br',
        'table', 'thead', 'tbody', 'tr', 'th', 'td'
    }
    allowed_attrs = bleach.ALLOWED_ATTRIBUTES.copy()
    allowed_attrs['*'] = ['class', 'style']
    clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)
    return clean_html

test_text = """
### Why the shift?
1. **Tactile Feedback**: Every keypress is a physical event.
2. **Durability**: Built to last for millions of strokes.
3. **Customization**: From switches to keycaps.

> "A good keyboard is the primary tool of the digital artisan."
"""

print(markdown_filter(test_text))
