# logrotate

Standalone Ansible role for Debian. Licensed under MIT. Authors: Zakariy Bouredji and Aymen Gazzah.

## Installation

```yaml
roles:
  - name: gazzah.logrotate
    src: https://github.com/gazzah-lab/ansible-role-logrotate.git
    version: v1.0.0
```

Run `ansible-galaxy role install -r requirements.yml`. Requires ansible-core >= 2.15, collected facts, and root privilege. Runtime smoke tests use Debian 13; other releases declared in metadata require validation in your environment.

## Inventory configuration

Store variables in `group_vars/all/gazzah.logrotate.yml`, override in group or host directories. These filenames are conventions: Ansible loads the variable contents.

```yaml
logrotate_configs:
- name: example
  paths:
  - /var/log/example/*.log
  options:
  - daily
  - rotate 7
  - missingok
  - notifempty
  - compress
```

The `manage_service` / `manage_systemd` false values above are for container tests; use their default true on real machines.

Each entry defines `name`, `paths`, and optional `options`, `create`, `postrotate`. Files are validated with `logrotate --debug` before replacement. Only marked files are removed. An empty list requires `logrotate_allow_empty: true`. Validation also runs with `--tags logrotate-cleanup`. Reserve foreign filenames with `logrotate_foreign_files`.

## Variables

| Variable | Default |
| --- | --- |
| `logrotate_packages` | `['logrotate']` |
| `logrotate_configs` | `[]` |
| `logrotate_config_dir` | `/etc/logrotate.d` |
| `logrotate_file_owner` | `root` |
| `logrotate_file_group` | `root` |
| `logrotate_file_mode` | `0644` |
| `logrotate_managed_marker` | `ANSIBLE MANAGED - gazzah.logrotate` |
| `logrotate_remove_orphans` | `True` |
| `logrotate_foreign_files` | `[]` |
| `logrotate_apt_install_state` | `present` |
| `logrotate_apt_update_cache` | `True` |
| `logrotate_apt_cache_valid_time` | `3600` |
| `logrotate_allow_empty` | `False` |

See [defaults/main.yml](defaults/main.yml) for comments and [tests/test.yml](tests/test.yml) for a runnable playbook.

## Testing

```sh
python -m pip install 'ansible-core>=2.20,<2.21' ansible-lint yamllint
yamllint -c .yamllint .
ansible-lint --offline -c .ansible-lint .
```

CI also runs the example twice in a disposable Debian 13 container and checks the second run has no changes. No automatic package upgrade, reboot, or cron job execution is triggered by these tests.
