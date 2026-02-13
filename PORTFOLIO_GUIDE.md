# Portfolio Management Guide

## Automatic Classification System

**NEW**: Portfolio items are now automatically categorized based on their 3-digit file name prefix! You no longer need to manually edit `_pages/portfolio.html`.

### Classification Rules

Portfolio files are automatically sorted into categories based on their number prefix:

| Prefix Range | Category | Description |
|-------------|----------|-------------|
| **000-199** | Category 1 | Atmospheric Dynamics & Meteorology |
| **200-299** | Category 2 | Estimation Theory & Machine Learning |
| **900-999** | Category 3 | Miscellaneous |

### Examples

- `050_Weather_Forecasts.md` → Category 1 (Atmospheric Dynamics)
- `101_traffic_jam_blocking.html` → Category 1 (Atmospheric Dynamics)
- `200_ensemble_conditional_gp.html` → Category 2 (ML)
- `997solitary_wave.html` → Category 3 (Miscellaneous)

## How Portfolio Items Work

This website uses Jekyll collections to manage portfolio items. Portfolio items are stored in the `_portfolio/` directory and are automatically generated into individual pages.

### File Naming Convention

Portfolio files in `_portfolio/` **must** follow this pattern:
- `NNN_descriptive_name.html` or `NNN_descriptive_name.md`
- Where `NNN` is a **3-digit number** that determines the category:
  - `000-199` for Atmospheric Dynamics & Meteorology
  - `200-299` for Estimation Theory & ML
  - `900-999` for Miscellaneous

Examples:
- `050_Weather_Forecasts.md` → Category 1
- `101_traffic_jam_blocking.html` → Category 1
- `200_ensemble_conditional_gp.html` → Category 2
- `997solitary_wave.html` → Category 3

### How Jekyll Generates URLs

Jekyll automatically converts file names to URLs:
- File: `050_Weather_Forecasts.md` → URL: `/portfolio/050_Weather_Forecasts/`
- File: `101_traffic_jam_blocking.html` → URL: `/portfolio/101_traffic_jam_blocking/`

## Adding New Portfolio Items

### Step 1: Choose the Right Number Prefix

Pick a 3-digit number based on the category:
- **000-199**: Atmospheric Dynamics & Meteorology
- **200-299**: Estimation Theory & Machine Learning  
- **900-999**: Miscellaneous

### Step 2: Create the Portfolio File

Create a new file in `_portfolio/` with the proper number prefix and name format:

**File name format**: `NNN_descriptive_name.html` or `NNN_descriptive_name.md`

Example: `150_my_new_research.html`

### Step 3: Add Front Matter

Add proper front matter to the file:

```yaml
---
title: "Your Project Title"
excerpt: "A brief description. Optional: add image with <img src='/images/your-image.png'>"
collection: portfolio
---

Your full project content goes here...
```

**Important**: If you want an image to display in the portfolio grid, include an `<img>` tag in the excerpt field.

### Step 4: Commit and Push

That's it! The portfolio page will **automatically**:
1. Detect the new file
2. Categorize it based on the number prefix
3. Display it in the appropriate modal
4. Extract and show the image from the excerpt (if provided)

**No manual editing of `portfolio.html` required!**

## Common Issues

### Issue: Portfolio item not showing up in any category

**Cause**: The file name doesn't start with a number in the correct range.

**Solution**: Ensure the file name starts with:
- `000-199` for Category 1 (Atmospheric Dynamics)
- `200-299` for Category 2 (Estimation Theory & ML)
- `900-999` for Category 3 (Miscellaneous)

Numbers outside these ranges won't appear in any category!

### Issue: Portfolio item appears in wrong category

**Cause**: The 3-digit prefix determines the category automatically.

**Solution**: Rename the file with the correct prefix:
- Want Category 1? Use `050_`, `100_`, `150_`, etc.
- Want Category 2? Use `200_`, `250_`, `299_`, etc.
- Want Category 3? Use `900_`, `950_`, `999_`, etc.

### Issue: Image not displaying in portfolio grid

**Cause**: The excerpt doesn't contain an `<img>` tag.

**Solution**: Add an image tag to the excerpt in your front matter:
```yaml
excerpt: "Your description <img src='/images/your-image.png'>"
```

## Portfolio Categories

The portfolio page has 3 categories with **automatic classification**:

1. **Atmospheric Dynamics & Meteorology** (modal1) - Files with prefix `000-199`
2. **Estimation Theory & Machine Learning** (modal2) - Files with prefix `200-299`
3. **Miscellaneous** (modal3) - Files with prefix `900-999`

Portfolio items are automatically sorted and displayed in the correct category based on their file name prefix. No manual configuration needed!

## Quick Start: Adding a Portfolio Item

1. **Choose a number**: Pick from 000-199, 200-299, or 900-999 based on the category
2. **Create file**: Upload to `_portfolio/` with name like `150_my_project.html`
3. **Add content**:
   ```yaml
   ---
   title: "My Project Title"
   excerpt: "Description <img src='/images/my-image.png'>"
   collection: portfolio
   ---
   
   Your content here...
   ```
4. **Commit**: Push to master branch
5. **Done**: Item automatically appears in the correct category!

## Checklist for Adding Portfolio Items

- [ ] File name starts with 3-digit number in correct range (000-199, 200-299, or 900-999)
- [ ] File name follows format: `NNN_descriptive_name.html` or `.md`
- [ ] Front matter includes: title, excerpt, and `collection: portfolio`
- [ ] Add image in excerpt if desired: `excerpt: "Text <img src='/images/pic.png'>"`
- [ ] File is in `_portfolio/` directory
- [ ] Commit and push to master branch
- [ ] Wait for GitHub Pages build (~1-3 minutes)
- [ ] Check the live site - item should appear automatically!

## Recent Updates (February 2026)

### Auto-Classification System (Latest)

**MAJOR UPDATE**: Portfolio items are now automatically categorized! 

- ✅ No need to edit `portfolio.html` manually
- ✅ Just upload files with correct number prefix
- ✅ System automatically detects and categorizes
- ✅ Images automatically extracted from excerpt field
- ✅ Items sorted by file name within each category

**How it works**: The portfolio page uses Jekyll Liquid to loop through all files in `_portfolio/` and automatically categorize them based on the 3-digit prefix (000-199, 200-299, or 900-999).

### Previous Fixes

Fixed several broken links where URLs didn't match file names:
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
