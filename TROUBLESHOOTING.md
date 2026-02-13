# Troubleshooting File Upload Issues

## Summary
This document provides guidance on resolving file upload and git commit issues in this repository.

## Verified Findings

After investigating the reported issue ("could no longer upload figs or files to anywhere"), we have verified that:

1. ✅ The `.gitignore` file is correct and not blocking any portfolio, image, or HTML files
2. ✅ Files can be successfully added to all directories (`files/`, `images/`, `_portfolio/`, etc.)
3. ✅ The popup centering fix in `_pages/portfolio.html` is working correctly and doesn't interfere with git operations
4. ✅ There are no git hooks or configurations preventing file uploads
5. ✅ The HTML syntax in `portfolio.html` is valid

## How to Add Files to This Repository

### Using Command Line (Git Bash/Terminal)

1. Navigate to your local repository:
   ```bash
   cd /path/to/yanxingjianken.github.io
   ```

2. Add your files:
   ```bash
   # Add a single file
   git add path/to/your/file.html
   
   # Add all files in a directory
   git add images/
   
   # Add all changed files
   git add .
   ```

3. Commit your changes:
   ```bash
   git commit -m "Add new portfolio content"
   ```

4. Push to GitHub:
   ```bash
   git push origin master
   ```

### Common Issues and Solutions

#### Issue: "Changes not staged for commit"
**Solution**: You need to explicitly add files with `git add <filename>`

#### Issue: "Nothing to commit, working tree clean"
**Solution**: All changes are already committed. Check if you saved your file edits.

#### Issue: "Permission denied"
**Solution**: Ensure you have write access to the repository or are authenticated properly.

#### Issue: Large files failing to upload
**Solution**: GitHub has a 100MB file size limit. Consider using Git LFS for files > 50MB.

### Files You Can Safely Add

- ✅ HTML files in `_portfolio/` directory
- ✅ Images in `images/` directory  
- ✅ Figures in `files/images/` directory
- ✅ Documents in `files/` directory
- ✅ Any markdown files in `_posts/` or `_pages/`

### Files That Are Ignored (by `.gitignore`)

- `_site/` - Jekyll build output
- `local/` - Local development files
- `Gemfile.lock` - Auto-generated file
- `node_modules/` - NPM dependencies
- `package-lock.json` - NPM lock file

## Next Steps

If you're still experiencing issues:

1. Check that your files are saved
2. Verify you're in the correct directory
3. Run `git status` to see which files have changes
4. Ensure your local repository is up to date: `git pull origin master`
5. Check for merge conflicts if pulling shows conflicts

## Specific File: `996_mid_freq_trading.html`

Note: This file now contains template content. To customize it:

1. Open the file in your editor: `_portfolio/996_mid_freq_trading.html`
2. Replace the placeholder text with your actual project content
3. Follow the format of other portfolio files (see `997solitary_wave.html` or `998pmdt_cv.html` as examples)
4. Save the file
5. Add, commit, and push as shown above

