# Design notes: Suds & Stats

The interface is a flat, light design built for a counter that is busy and often viewed on a tablet or phone.

## Layout
- A dark slate sidebar for navigation, a light page, and white cards with a thin border and a soft shadow.
- On screens narrower than 800 px the sidebar becomes a slide-in menu and order tables turn into cards,
  so nothing needs sideways scrolling on a phone.

## Colors
| Use | Color |
|---|---|
| Page | `#f6f8fa` |
| Cards | white, border `#e2e8f0` |
| Text | `#0f172a`, secondary `#64748b` |
| Accent (buttons, links, active items) | blue `#2563eb`, changeable in Shop settings |
| Waiting | amber `#f59e0b` |
| Washing | blue `#2563eb` |
| Ready for pickup | green `#16a34a` |
| Turnaround | Standard grey, Express blue, Rush red |

Status colors stay fixed whatever accent a shop picks, so a color always means the same thing.

## Type
Inter (bundled in `frontend/static/fonts/`), 14 px body text. Table text is 13 px and nothing is smaller than 11 px.

## Washer graphic
The Next up card on the service queue shows a washing machine. Its drum turns while a bag is waiting to be washed and
stops when the line is empty. It is plain SVG and CSS, and the animation is switched off for people who ask their device
for reduced motion.

## Files
- `frontend/static/app.css` holds every style.
- `frontend/templates/` holds the pages.
- `backend/workspace/templatetags/ui.py` holds the icons and the `peso` and `kilos` display filters.
