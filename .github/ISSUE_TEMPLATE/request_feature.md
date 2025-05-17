---
# NOTE: this file is managed by terraform

name: 💡 Feature Request
description: Request a feature or feature change
title: 'feature: '
body:
  - type: textarea
    attributes:
      label: Describe the Feature Request
      description: A clear and concise description of what the feature does.
    validations:
      required: true
  - type: textarea
    attributes:
      label: Describe the Use Case
      description: A clear and concise use case for what problem this feature would solve.
    validations:
      required: true
  - type: textarea
    attributes:
      label: Additional Information
      description: List any other information that is relevant to your issue.
        Stack traces, related issues, suggestions on how to implement, Stack Overflow links, forum links, etc.
        Please upload any screenshots that your think are relevant.
  - type: markdown
    attributes:
      value: |
        Thank you for your time and effort!
