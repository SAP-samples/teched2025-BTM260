# BTM260 - Building AI agents on your SAP LeanIX solutions with Model Context Protocol (MCP)

## Description

This repository contains the material for the SAP TechEd 2025 session BTM260 - Building AI agents on your SAP LeanIX solutions with Model Context Protocol (MCP).

## Overview

In this session, we show you how to leverage the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) to access information in your LeanIX workspace. We will use a demo workspace for this purpose which is already filled with demo data describing the IT landscape of a fictional company. The screenshot below shows how your LeanIX workspace looks like in the beginning of this exercise.

![LeanIX screenshot](./images/leanix-screenshot.png)

We leverage the LeanIX MCP Server to connect AI Agents built in code with the data in the LeanIX workspace. Furthermore, we will show how this can be easily combined with MCP Servers from 3rd parties thus being able to contextualize data from these systems with your Enterprise Architecture source of truth.

The following picture shows the anticipated architecture. You will work on the colored components. All other components will be provided by us.

![MCP Overview](./images/mcp-ai-app.drawio.svg)

## Requirements

In order to be able to follow the exercises in this repository, you need:

1. VSCode with Jupyter extension
2. Python installation
3. Access to SAP BTP AI Core GenAI Hub with deployment of gpt-4.1
4. Admin access to a LeanIX workspace

All of this will be provided to TechEd 2025 onsite session participants.

## Install dependencies

Create & activate a virtual environment, install deps, register kernel:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name teched-workshop
```

## Exercises

- Exercise 1 - [Basic AI Agent loop](./exercises/ex1/ex1-basics.ipynb)
- Exercise 2 - [Build Employee Portal Chatbot](./exercises/ex2/ex2-build-employee-portal-chatbot.ipynb)

## Contributing

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) to understand contribution guidelines.

## Code of Conduct

Please read the [SAP Open Source Code of Conduct](https://github.com/SAP-samples/.github/blob/main/CODE_OF_CONDUCT.md)

## License

Copyright (C) 2025 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](./LICENSES/Apache-2.0.txt) file.
