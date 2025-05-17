---
# NOTE: this file is managed by terraform

name: 🐛 Bug Report
description: Create a report to help us improve this project.
title: 'bug: '
body:
  - type: textarea
    attributes:
      label: Version
      description: Please select which versions this issue impacts.
  - type: textarea
    attributes:
      label: Current Behavior
      description: A clear description of what the bug is and how it manifests.
    validations:
      required: true
  - type: textarea
    attributes:
      label: Expected Behavior
      description: A clear description of what you expected to happen.
    validations:
      required: true
  - type: textarea
    attributes:
      label: Steps to Reproduce
      description: Please explain the steps required to reproduce this issue.
    validations:
      required: true
  - type: textarea
    attributes:
      label: Additional Information
      description: List any other information that is relevant to your issue. Stack traces, related issues,
        suggestions on how to fix, Stack Overflow links, forum links, etc.
        Please upload any screenshots that your think are relevant.
  - type: markdown
    attributes:
      value: |
        Thank you for your time and effort!
