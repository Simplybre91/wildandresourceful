# Wild & Resourceful

Blog site for wildandresourceful.com, hosted on Cloudflare Pages (deploys automatically on every push to `main`).

## Adding a post
1. Add `_src/posts/<slug>.html`: a JSON header inside `<!-- -->` (slug, cat, date, read, title, dek, tags, photo, photoCaption, next), then the post body in HTML.
2. Run `python3 _src/build.py`. It rebuilds every page, `posts.json`, `sitemap.xml` and `robots.txt`.
3. Commit and push. Cloudflare publishes it in about a minute.

Categories: Outdoors, Tech, Trades, Shopping, AI, Deals, Travel.
Subscribe form: set `SUBSCRIBE_URL` in `assets/site.js` once the email service is set up.
