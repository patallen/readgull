## ReadGull Static Site Generator

A static site generator written in python. Like Pelican, but uses custom content types.

## Overview
**Rules**:
1. All content will be available through the global context.
    - e.g. Articles can be available on the home page and a project page.
1. The user will be able to configure each content type to fit his/her needs.

### Content Types
A user will be able to define the content types (e.g. Projects, Articles, Recipes) that will have properties and configurations defined by the user.

These content types will be configureable as such:

    - Default Values
    - Required Values
    - Plural Content Type Name
    - Input folder (defaults to content type name)
    - Output folder(default sto content type name within content folder)
    - Reader type (markdown/rst/...)
    - Order by (date/alphabetically/...)
