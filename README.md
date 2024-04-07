# Building the Website

This repository is now managed by the buildbot, streamlining the process of generating and publishing the website. All you need to do is update the markdown files, and the buildbot will handle the rest.

## Prerequisites

Before proceeding, ensure you have the following:

* Python 3 installed on your system.
* The markdown module for Python 3. If you haven't installed it yet, you can do so by running the following command:
  ```
  sudo pip3 install markdown
  ```

## Instructions

To build the website, follow these simple steps:

1. **Edit or Create Markdown Files:** 
   Navigate to the `source/` directory within the repository. Here, you'll find markdown files for the website content. Feel free to edit existing files or create new ones. You can organize files into subdirectories within `source/` as needed.

2. **Generate the Website:**
   Open a shell and navigate to the `source/` directory. Once there, run the following command to generate the website:
   ```
   python3 generate.py
   ```

3. **Commit Changes to Git:**
   After generating the website, commit your changes to Git. Make sure to include any modifications or additions you've made to the markdown files.

That's it! The buildbot will automatically regenerate the site based on your changes and publish it accordingly.

Thank you for contributing to the website! If you have any questions or encounter any issues, feel free to reach out.