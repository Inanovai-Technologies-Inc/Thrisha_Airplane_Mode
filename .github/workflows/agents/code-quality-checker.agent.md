---
name: Code Quality Checker
description: Checks code for simple issues such as unused variables and unused imports.
---

# Code Quality Checker

Review the code in the repository for simple code-quality issues.

Check for:

- Variables that are declared but never used.
- Imports that are added but never used.
- Functions or methods that are clearly unused.
- Unreachable or obviously dead code.
- Simple syntax or coding mistakes.

For every issue found, report:

- File name
- Line number
- Issue
- Suggested fix

Do not modify any files.

Do not report formatting or subjective style preferences.

Do not report an issue unless there is clear evidence that it exists.

If no issues are found, say:

"No issues found."