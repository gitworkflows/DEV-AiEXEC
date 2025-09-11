# 🛡️ Aiexec Security Policy & Responsible Disclosure

## Security Policy

This security policy applies to all public projects under the khulnasoft-lab organization on GitHub. We prioritize security and continuously work to safeguard our systems. However, vulnerabilities can still exist. If you identify a security issue, please report it to us so we can address it promptly.

### Security/Bugfix Versions

- Fixes are released either as part of the next minor version (e.g., 1.3.0 → 1.4.0) or as an on-demand patch version (e.g., 1.3.0 → 1.3.1)
- Security fixes are given priority and might be enough to cause a new version to be released

## Reporting a Vulnerability

We encourage responsible disclosure of security vulnerabilities. If you find something suspicious, we encourage and appreciate your report!

### How to Report

Use the "Report a vulnerability" button under the "Security" tab of the [Aiexec GitHub repository](https://github.com/khulnasoft-lab/aiexec/security). This creates a private communication channel between you and the maintainers.

### Reporting Guidelines

- Provide clear details to help us reproduce and fix the issue quickly
- Include steps to reproduce, potential impact, and any suggested fixes
- Your report will be kept confidential, and your details will not be shared without your consent

### Response Timeline

- We will acknowledge your report within 5 business days
- We will provide an estimated resolution timeline
- We will keep you updated on our progress

### Disclosure Guidelines

- Do not publicly disclose vulnerabilities until we have assessed, resolved, and notified affected users
- If you plan to present your research (e.g., at a conference or in a blog), share a draft with us at least 30 days in advance for review
- Avoid including:
  - Data from any Aiexec customer projects
  - Aiexec user/customer information
  - Details about Aiexec employees, contractors, or partners

We appreciate your efforts in helping us maintain a secure platform and look forward to working together to resolve any issues responsibly.

## Known Vulnerabilities

### Code Execution Vulnerability (Fixed in 1.3.0)

Aiexec allows users to define and run **custom code components** through endpoints like `/api/v1/validate/code`. In versions < 1.3.0, this endpoint did not enforce authentication or proper sandboxing, allowing **unauthenticated arbitrary code execution**.

This means an attacker could send malicious code to the endpoint and have it executed on the server—leading to full system compromise, including data theft, remote shell access, or lateral movement within the network.

**CVE**: [CVE-2025-3248](https://nvd.nist.gov/vuln/detail/CVE-2025-3248)
**Fixed in**: Aiexec >= 1.3.0

### Privilege Escalation via CLI Superuser Creation (Fixed in 1.5.1)

A privilege escalation vulnerability exists in Aiexec containers where an authenticated user with RCE access can invoke the internal CLI command `aiexec superuser` to create a new administrative user. This results in full superuser access, even if the user initially registered through the UI as a regular (non-admin) account.

**CVE**: [CVE-2025-57760](https://github.com/khulnasoft-lab/aiexec/security/advisories/GHSA-4gv9-mp8m-592r)
**Fixed in**: Aiexec >= 1.5.1

### No API key required if running Aiexec with `AIEXEC_AUTO_LOGIN=true` and `AIEXEC_SKIP_AUTH_AUTO_LOGIN=true`

In Aiexec versions earlier than 1.5, if `AIEXEC_AUTO_LOGIN=true`, then Aiexec automatically logs users in as a superuser without requiring authentication. In this case, API requests don't require a Aiexec API key.

In Aiexec version 1.5, a Aiexec API key is required to authenticate requests.
Setting `AIEXEC_SKIP_AUTH_AUTO_LOGIN=true` and `AIEXEC_AUTO_LOGIN=true` skips authentication for API requests. However, the `AIEXEC_SKIP_AUTH_AUTO_LOGIN` option will be removed in v1.6.

`AIEXEC_SKIP_AUTH_AUTO_LOGIN=true` is the default behavior, so users do not need to change existing workflows in 1.5. To update your workflows to require authentication, set `AIEXEC_SKIP_AUTH_AUTO_LOGIN=false`.

For more information, see [API keys and authentication](https://docs.khulnasoft.com/api-keys-and-authentication).

## Security Configuration Guidelines

### Superuser Creation Security

The `aiexec superuser` CLI command can present a privilege escalation risk if not properly secured.

#### Security Measures

1. **Authentication Required in Production**
   - When `AIEXEC_AUTO_LOGIN=false`, superuser creation requires authentication
   - Use `--auth-token` parameter with a valid superuser API key or JWT token

2. **Disable CLI Superuser Creation**
   - Set `AIEXEC_ENABLE_SUPERUSER_CLI=false` to disable the command entirely
   - Strongly recommended for production environments

3. **Secure AUTO_LOGIN Setting**
   - Default is `true` for <=1.5. This may change in a future release.
   - When `true`, creates default superuser `aiexec/aiexec` - **ONLY USE IN DEVELOPMENT**

#### Production Security Configuration

```bash
# Recommended production settings
export AIEXEC_AUTO_LOGIN=false
export AIEXEC_ENABLE_SUPERUSER_CLI=false
export AIEXEC_SUPERUSER="<your-superuser-username>"
export AIEXEC_SUPERUSER_PASSWORD="<your-superuser-password>"
export AIEXEC_DATABASE_URL="<your-production-database-url>" # e.g. "postgresql+psycopg://aiexec:secure_pass@db.internal:5432/aiexec"
export AIEXEC_SECRET_KEY="your-strong-random-secret-key"
```
