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
- The main screens are `index.html` (sign-in), `main.html` (library and playback), and `file_upload.html` (uploads). They share `WebVideoPlayer/static/css/app-ui.css`; keep shared visual tokens and responsive behavior there rather than duplicating inline styles.
- `utils.js` builds the movie, show, and season lists dynamically. Preserve the mount points `video_files`, `shows_files`, `season_files`, and `episodeListPlayer`, along with the modal mount points and existing scan/upload event handlers.
- Playback uses the `video_hls` element initialized by the existing HLS script. Keep its ID, subtitle tracks, and playback URL contract intact when restyling the player.
- The primary application static source directory is `WebVideoPlayer/static/`; the repository-root `static/` directory contains a separate collected/legacy asset tree. Avoid copying app changes into that tree unless deployment configuration specifically requires it.
