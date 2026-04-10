# mdabbas-profile

Static multi-page portfolio site for Mohamed Abbas Moynudeen, built for GitHub Pages deployment.

## Local preview

Open `index.html` directly in a browser, or run a simple static server:

```powershell
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploy to GitHub Pages

1. Push this repository to GitHub.
2. Open the repository settings.
3. Go to `Pages`.
4. Set the source to `Deploy from a branch`.
5. Select the `main` branch and `/ (root)` folder.
6. Save. GitHub will publish the site using `index.html`.

## Files

- `index.html` - home page
- `projects/` - project hub and detailed project pages
- `styles.css` - shared visual design and responsive layout
- `script.js` - reveal animations and page-level navigation state
- `IMG/` - place `profile.jpg` or `profile.png` here for the hero portrait
- `Md_Abbas_20250825_215203_0000.pdf` - downloadable resume
