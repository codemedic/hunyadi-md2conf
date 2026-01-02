# Release Process

This document describes the release process for md2conf, including version numbering, tagging conventions, and publishing workflows.

## Version Numbering

We follow [Semantic Versioning](https://semver.org/) and [PEP 440](https://www.python.org/dev/peps/pep-0440/).

### Pre-Release Versions

- **Alpha** (`v0.6.0a1`, `v0.6.0a2`): Early testing phase, API may change
- **Beta** (`v0.6.0b1`, `v0.6.0b2`): Feature complete, stabilization phase
- **Release Candidate** (`v0.6.0rc1`, `v0.6.0rc2`): Final testing before stable release

### Stable Versions

- **Patch** (`v0.6.1`): Bug fixes, no new features
- **Minor** (`v0.7.0`): New features, backward compatible
- **Major** (`v1.0.0`): Breaking changes

## Branch Protection

**Critical:** Production version tags can ONLY be created on the `master` branch.

| Tag Type | Branch Restriction | Workflow Behavior |
|----------|-------------------|-------------------|
| Production (`v*.*.*`, `v*.*.*a1`, `v*.*.*rc1`) | master only | Validates branch, fails if not on master |
| Test (`v*.*.*-test`) | any branch | Workflows don't trigger (excluded) |

This prevents accidental releases from feature branches while allowing safe workflow testing.

## Creating Releases

### Prerequisites

```bash
# Ensure you're on master and up-to-date
git checkout master
git pull upstream master

# Run quality checks
source .venv/bin/activate
./check.sh
```

### Alpha Release

```bash
git tag -a v0.6.0a1 -m "Alpha 1 for version 0.6.0"
git push upstream v0.6.0a1
```

**What happens:**
- Publishes to PyPI (marked as pre-release, hidden by default)
- Builds and pushes Docker images with `0.6.0a1` tags
- Does NOT update `latest` Docker tag
- Does NOT create major version tag (`v0`)

### Beta Release

```bash
git tag -a v0.6.0b1 -m "Beta 1 for version 0.6.0"
git push upstream v0.6.0b1
```

**What happens:** Same as alpha, with beta version tag.

### Release Candidate

```bash
git tag -a v0.6.0rc1 -m "Release Candidate 1 for version 0.6.0"
git push upstream v0.6.0rc1
```

**What happens:** Same as alpha/beta, with RC version tag.

### Stable Release

```bash
git tag -a v0.6.0 -m "Release version 0.6.0"
git push upstream v0.6.0
```

**What happens:**
- Publishes to PyPI (default, visible to all users)
- Builds and pushes Docker images with `0.6.0` tags
- Updates `latest` Docker tag
- Creates/updates major version tag (`v0`)

## Installing Pre-Releases

```bash
# Default: only stable releases
pip install markdown-to-confluence

# Include pre-releases
pip install --pre markdown-to-confluence

# Specific pre-release version
pip install markdown-to-confluence==0.6.0a1
```

## Testing Workflows

### Test Tags (No Publishing)

For testing workflow changes on feature branches:

```bash
# Create test tag (workflows won't trigger)
git tag v0.6.0-test
git push origin v0.6.0-test

# Cleanup
git tag -d v0.6.0-test
git push origin --delete v0.6.0-test
```

### Manual Docker Builds

For testing Docker builds without publishing:

```bash
gh workflow run publish-docker.yml \
  --ref your-feature-branch \
  -f push_images=false
```

## What Gets Published

| Release Type | PyPI | Docker Hub | Docker `latest` | Major Tag (`v0`) |
|--------------|------|------------|-----------------|------------------|
| Test (`-test`) | No | No | No | No |
| Alpha (`a1`) | Yes* | Yes | No | No |
| Beta (`b1`) | Yes* | Yes | No | No |
| RC (`rc1`) | Yes* | Yes | No | No |
| Stable | Yes | Yes | Yes | Yes |

\* Pre-releases are published to PyPI but hidden by default (users must use `--pre` flag)

## Expected Docker Tags

### Pre-release (v0.6.0a1)
```
leventehunyadi/md2conf:0.6.0a1
leventehunyadi/md2conf:0.6.0a1-minimal
leventehunyadi/md2conf:0.6.0a1-mermaid
leventehunyadi/md2conf:0.6.0a1-plantuml
```

### Stable (v0.6.0)
```
leventehunyadi/md2conf:0.6.0
leventehunyadi/md2conf:0.6.0-minimal
leventehunyadi/md2conf:0.6.0-mermaid
leventehunyadi/md2conf:0.6.0-plantuml
leventehunyadi/md2conf:latest          # Only for stable
leventehunyadi/md2conf:latest-minimal
leventehunyadi/md2conf:latest-mermaid
leventehunyadi/md2conf:latest-plantuml
leventehunyadi/md2conf:0               # Major version alias
```

## Safety Features

1. **Branch Validation**: Production tags require master branch
2. **Pre-release Isolation**: Alpha/beta/RC hidden from default pip installs
3. **Docker Latest Protection**: `latest` tag only updates for stable releases
4. **Major Version Stability**: Major version tags (e.g., `v0`) only point to stable releases
5. **Test Tag Exclusion**: Test tags (`-test` suffix) don't trigger production workflows

## Testing PyPI Publishing (Forked Repositories)

Forked repositories can test PyPI publishing without affecting the production package by using TestPyPI.

### Configuration

1. **Register for TestPyPI:**
   - Create account: https://test.pypi.org/account/register/
   - Generate API token: https://test.pypi.org/manage/account/token/

2. **Configure GitHub Repository:**
   - **Secret:** `TEST_PYPI_API_TOKEN` = your TestPyPI token
   - **Variable:** `PYPI_TARGET` = `testpypi`

3. **Test Publishing:**
   ```bash
   git checkout master
   git tag v0.5.2rc1
   git push origin v0.5.2rc1
   ```

4. **Verify:**
   - View: https://test.pypi.org/project/markdown-to-confluence/
   - Install: `pip install --index-url https://test.pypi.org/simple/ markdown-to-confluence==0.5.2rc1`

**Note:** TestPyPI is completely separate from production PyPI. Publishing there has no effect on the real package.

## Troubleshooting

### Error: "Production version tags must be created on master/main branch"

You attempted to push a production tag from a feature branch. Solutions:

1. **Merge to master first:**
   ```bash
   # Create PR, get approved, merge to master
   git checkout master
   git pull upstream master
   git tag v0.6.0
   git push upstream v0.6.0
   ```

2. **Use test tag for workflow testing:**
   ```bash
   git tag v0.6.0-test
   git push origin v0.6.0-test
   ```

### Pre-release not visible on PyPI

This is expected. Pre-releases are hidden by default. Users must explicitly request them:

```bash
pip install --pre markdown-to-confluence
# or
pip install markdown-to-confluence==0.6.0a1
```

### Docker `latest` not updating

`latest` only updates for stable releases (not alpha/beta/RC). This is intentional to protect users from unstable versions.

## Automated Workflows

Three GitHub Actions workflows handle releases:

1. **publish-python.yml**: Builds and publishes Python package to PyPI
2. **publish-docker.yml**: Builds and publishes Docker images to Docker Hub
3. **tag-alias.yml**: Creates/updates major version tags for stable releases

All workflows include branch validation and pre-release detection.
