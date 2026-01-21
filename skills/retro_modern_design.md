# Retro Modern Design System

## Purpose
Maintain visual consistency with the "Retro Tech Archive" aesthetic throughout the application's frontend.

## When to Use
- When creating or modifying Jinja2 templates (`app/templates/`).
- When updating CSS (`app/static/css/main.css`).
- When adding new UI components.

## Rules
1. **Color Palette:** Use only variables defined in `:root`:
   - `--bg-color: #F5F1EA` (Background)
   - `--primary-color: #4A5D4E` (Moss Green)
   - `--secondary-color: #2F4F4F` (Petroleum Blue)
   - `--text-color: #1E1E1E`
2. **Typography:**
   - Serif (`Merriweather`): Main body text and logo.
   - Sans-serif (`Inter`): UI elements and headings.
   - Monospace (`IBM Plex Mono`): Code blocks.
3. **UI Elements:** Use the `card` class for content blocks and `btn-primary` for main actions.

## Constraints
- Do not introduce bright or neon colors.
- Maintain the "academic archive" look: clean, minimal, and high-contrast text.

## Expected Output
Templates and CSS that use the established CSS variables and classes, ensuring the new UI looks integrated with the existing site.
