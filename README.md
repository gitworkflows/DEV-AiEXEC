<!-- markdownlint-disable MD030 -->

# 🚀 Aiexec

[![Release Notes](https://img.shields.io/github/release/khulnasoft-lab/aiexec?style=flat-square)](https://github.com/khulnasoft-lab/aiexec/releases) [![PyPI - License](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT) [![PyPI - Downloads](https://img.shields.io/pypi/dm/aiexec?style=flat-square)](https://pypistats.org/packages/aiexec) [![GitHub star chart](https://img.shields.io/github/stars/khulnasoft-lab/aiexec?style=flat-square)](https://star-history.com/#khulnasoft-lab/aiexec) [![Open Issues](https://img.shields.io/github/issues-raw/khulnasoft-lab/aiexec?style=flat-square)](https://github.com/khulnasoft-lab/aiexec/issues) [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/aiexec-ai.svg?style=social\&label=Follow%20%40Aiexec)](https://twitter.com/khulnasoft)

**Aiexec** is a powerful framework for building and deploying AI-powered agents and workflows. It combines a **visual builder**, **Python source code access**, and **built-in API/MCP servers**, turning every workflow into a tool that can integrate seamlessly with any application, framework, or stack.

Aiexec comes with **batteries included**, supporting all major **LLMs, vector databases**, and a growing library of AI tools.

---


## ✨ Features

* 🖥️ **Visual Builder** — Quickly design and iterate workflows with an intuitive interface.
* 🐍 **Python Customization** — Access source code and extend any component.
* 🎮 **Interactive Playground** — Test and refine flows step by step.
* 🤖 **Multi-Agent Orchestration** — Manage conversations and retrieval across agents.
* 📡 **Deployment Options**

  * Export as JSON for Python apps
  * Deploy as REST API
  * Run as an **MCP server** (flows as MCP tools)
* 🔍 **Observability** — Integrations with LangSmith, LangFuse, and more.
* 🛡️ **Enterprise Security**

  * Automated security scanning (Bandit, Safety)
  * Dependency checks & secure defaults
  * Vulnerability scanning & secure coding practices

---

## ⚡ Quickstart

### Installation

```bash
pip install aiexec -U
```

### Run Aiexec

```bash
uv run aiexec run
```

Open your browser at: [http://127.0.0.1:7860](http://127.0.0.1:7860)

➡️ For Docker and Desktop installation options, see the Install Guide.

### 🔒 Security

Aiexec prioritizes security with:

* ✅ Automated Security Scanning (Bandit & Safety)
* 📦 Dependency Management & regular updates
* 🔐 Secure Defaults for authentication & authorization
* 📢 Responsible Disclosure via our Security Policy

For full details, see the Security Documentation and Development Security Guide.

### 📦 Deployment

Aiexec is open source and deployable to all major cloud providers. Follow the Docker Deployment Guide for containerized setup.

Security Best Practices:

* Always use the latest version
* Run security scans in CI/CD pipelines
* Keep dependencies updated
* Follow least privilege principle
* Use environment variables for secrets

### ❤️ Contributors

* [KhulnaSoft Lab](https://github.com/khulnasoft-lab)

### 🌐 Resources

* Documentation
* Installation Guide
* Deployment Guides
* Security

### 📜 License

Aiexec is licensed under the MIT License.
