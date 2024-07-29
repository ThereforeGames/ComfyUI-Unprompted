# Changelog
All notable changes to this project will be documented in this file.

<details><summary>0.2.2 - 29 July 2024</summary>

### Added
- Support Unprompted v11.2.0

</details>

<details><summary>0.2.1 - 23 June 2024</summary>

### Fixed
- Resolved an issue with `install.py` package upgrade logic

</details>

<details><summary>0.2.0 - 23 June 2024</summary>

### Added
- New input `anything`: connect any node to this input (for example, an image) and it will be made accessible in your Unprompted string as a variable
- New widget `set_anything_to`: the variable name to use for the `anything` input (defaults to `comfy_var`)
- New output `IMAGE`: Unprompted can now return an image contained in a variable of your choosing (in the future, I may extend this to additional data types - but for now I think `STRING`and `IMAGE` are the most useful)
- New widget `return_image_var`: the variable that contains the output image (defaults to `comfy_var`)
- The Unprompted object's `webui` variable is now `comfy`, making it easier for shortcodes to implement ComfyUI support

### Changed
- The Node version is now shown in the header instead of the Unprompted language version

</details>

<details><summary>0.1.1 - 7 June 2024</summary>

### Fixed
- Speculative fixes for ComfyUI Manager support

</details>

<details><summary>0.1.0 - 5 June 2024</summary>

### Added
- New setting `always_rerun` to force the node to re-run even when the input data hasn't changed

</details>

<details><summary>0.0.1 - 4 June 2024</summary>

### Added
- Initial release

</details>