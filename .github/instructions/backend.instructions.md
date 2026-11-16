---
applyTo: "WebVideoPlayer/**/*.py"
---

# Backend instructions

- The Django project is in `WebVideoPlayer/`; the `video_player` and `utils` apps contain the main playback, media-library, upload, and account logic.
- Follow the installed Django version range in `requirements.txt` and existing project conventions. Keep URL routing in the relevant app's `urls.py` and view logic in that app.
- Preserve existing request, session, template-context, and JSON response contracts when changing views; update the corresponding frontend integration when a contract must change.
- Protect views that expose user or media data using the existing session/permission conventions. Validate request data and file paths before filesystem operations; never trust a client-supplied path.
- For model/schema changes, create a new Django migration rather than editing an existing migration. Add or update focused tests in the relevant app's `tests.py`.
- Use Django ORM operations and existing logging conventions. Avoid logging credentials, uploaded file contents, or other sensitive data.
- Settings, URL routing, and WSGI/ASGI configuration belong to the inner `WebVideoPlayer/WebVideoPlayer/` package. Do not put secrets in source or commit generated databases, logs, or media files.
- The frontend's dynamic library calls use `/utils/list_items` with `type` and `category` or `uuid` query parameters. Keep its JSON shape aligned with `utils/views.py` and the consumers in `WebVideoPlayer/static/js/utils.js`.
- `BASE_DIR` resolves to the inner `WebVideoPlayer/` directory, and `STATIC_ROOT` points to its `static/` directory; app templates and static discovery use Django's app directories.
- Validation caveat observed in the current checkout: `python manage.py check` expects `WebVideoPlayer/logs/` to exist for configured file handlers, and importing `video_player.views` requires `psutil`, which is not listed in `requirements.txt`. Keep these environment/setup blockers distinct from UI or template failures.
