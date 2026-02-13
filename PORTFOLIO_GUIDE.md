# Portfolio Management Guide

## How Portfolio Items Work

This website uses Jekyll collections to manage portfolio items. Portfolio items are stored in the `_portfolio/` directory and are automatically generated into individual pages.

### File Naming Convention

Portfolio files in `_portfolio/` should follow this pattern:
- `NNN_descriptive_name.html` or `NNN_descriptive_name.md`
- Where `NNN` is a number for sorting (e.g., `050`, `100`, `101`)

Examples:
- `050_Weather_Forecasts.md`
- `101_traffic_jam_blocking.html`
- `200_ensemble_conditional_gp.html`

### How Jekyll Generates URLs

Jekyll automatically converts file names to URLs:
- File: `050_Weather_Forecasts.md` → URL: `/portfolio/050_Weather_Forecasts/`
- File: `101_traffic_jam_blocking.html` → URL: `/portfolio/101_traffic_jam_blocking/`

## Adding New Portfolio Items

### Step 1: Create the Portfolio File

Create a new file in `_portfolio/` with proper front matter:

```html
---
title: "Your Project Title"
excerpt: "A brief description that appears in listings"
collection: portfolio
---

Your full project content goes here...
```

### Step 2: Add to Portfolio Page

Edit `_pages/portfolio.html` to add a link in the appropriate modal section.

**Important**: The URL must match the file name exactly!

Example:
```html
<div class="plot-item">
  <a href="{{ base_path }}/portfolio/YOUR_FILE_NAME/">
    <img src="{{ base_path }}/images/your-image.png" alt="Description" class="plot-image">
    <div class="plot-title">Your Project Title</div>
  </a>
</div>
```

If you have no image, use:
```html
<div class="plot-item">
  <a href="{{ base_path }}/portfolio/YOUR_FILE_NAME/">
    <div class="no-image">No plot available</div>
    <div class="plot-title">Your Project Title</div>
  </a>
</div>
```

### Step 3: Commit and Push

After editing via GitHub's web interface or locally:
1. Commit your changes
2. Push to the master branch
3. GitHub Pages will automatically rebuild (takes 1-3 minutes)
4. Visit your site to see the changes

## Common Issues

### Issue: Portfolio item not showing up

**Cause**: The link in `_pages/portfolio.html` doesn't match the actual file name.

**Solution**: Check that:
1. The file name in `_portfolio/` matches exactly
2. The URL in portfolio.html uses the correct file name
3. Example: If file is `050_Weather_Forecasts.md`, URL must be `/portfolio/050_Weather_Forecasts/`

### Issue: Changes not appearing on live site

**Cause**: GitHub Pages build may be in progress or failed.

**Solution**:
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Check the "pages build and deployment" workflow
4. Wait for it to complete (green checkmark)
5. If it fails (red X), click to see error details

### Issue: 404 error when clicking portfolio item

**Cause**: Missing or misnamed file in `_portfolio/` directory.

**Solution**:
1. Check that the file exists in `_portfolio/`
2. Verify the file has proper front matter with `collection: portfolio`
3. Ensure the link in portfolio.html matches the file name exactly

## Portfolio Categories

The portfolio page has 3 categories:

1. **Atmospheric Dynamics & Meteorology** (modal1)
2. **Estimation Theory & Machine Learning** (modal2)
3. **Miscellaneous** (modal3)

Add your portfolio item to the appropriate modal section in `_pages/portfolio.html`.

## Checklist for Adding Portfolio Items

- [ ] Create file in `_portfolio/` with proper naming
- [ ] Add front matter with title, excerpt, and collection
- [ ] Add content to the file
- [ ] Add link in `_pages/portfolio.html` matching the exact file name
- [ ] Choose appropriate category (modal1, modal2, or modal3)
- [ ] Add image or use "no-image" placeholder
- [ ] Commit changes
- [ ] Wait for GitHub Pages build to complete
- [ ] Test the link on the live site

## Recent Fixes (February 2026)

Fixed several broken links where the URLs in portfolio.html didn't match actual file names:
- Fixed: `001_Weather_Forecasts` → `050_Weather_Forecasts`
- Fixed: `995RWB_blocking_termination` → `102_RWB_blocking_termination`
- Fixed: `996blocking` → `101_traffic_jam_blocking`
- Fixed: `994_XTC_downscaling` → `201_XTC_downscaling`
- Fixed: `993_ensemble_conditional_gp` → `200_ensemble_conditional_gp`
- Added: Missing portfolio item `100_4_bases`

## Need Help?

If portfolio items still aren't showing up:
1. Check the GitHub Actions workflow status
2. Verify file names match URLs exactly
3. Check Jekyll build logs for errors
4. Review this guide's troubleshooting section
