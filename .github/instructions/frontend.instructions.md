---
applyTo: "WebVideoPlayer/video_player/templates/**/*.html,WebVideoPlayer/static/**/*.css,WebVideoPlayer/static/**/*.js,static/**/*.css,static/**/*.js"
---

# Frontend instructions

- The UI is server-rendered with Django templates under `WebVideoPlayer/video_player/templates/`. Preserve the existing template context and URL contracts with the Django views when changing pages.
- Frontend assets live in `WebVideoPlayer/static/` and in the root `static/` collected-assets tree. Prefer editing the app's source assets; update the collected copy only when the change clearly belongs there.
- Existing pages use Bootstrap, jQuery, Video.js, HLS.js, and Epub.js. Reuse the libraries already present and do not replace or edit vendored/minified dependencies for application changes.
- Keep markup, CSS, and JavaScript compatible with the project's existing browser-side patterns. Avoid introducing a build system or frontend dependency without a clear need.
- Use Django template URL/static helpers where appropriate, preserve CSRF protection on state-changing forms, and rely on template autoescaping for dynamic values. Do not construct HTML from untrusted values without safe escaping.
- Keep playback, upload, and library-browsing interactions consistent with the server endpoints and data shape they already consume.
