# Automate unicorn via AAP

## Prerequisites

- AAP 2.5
- RHEL 9.5 to reach unicorn API
  - Enable Ansible Repository
    - `subscription-manager repos --enable=ansible-automation-platform-2.5-for-rhel-9-x86_64-rpms`
  - Install Ansible
    - `dnf -y install receptor`
  - Download collection receptor
    - `ansible-galaxy collection install ansible.receptor`

All at once

```bash
subscription-manager repos --enable=ansible-automation-platform-2.5-for-rhel-9-x86_64-rpms
dnf -y install receptor
ansible-galaxy collection install ansible.receptor
```

## Setup

### Execution node setup

Download installation bundle as [described in the documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/installing_on_openshift_container_platform/operator-add-execution-nodes_operator-platform-doc#operator-add-execution-nodes_operator-platform-doc).

### Automation Controller setup

#### Create Project

- Name: *Automated Unicorn*
- Source Control Type: *Git*
- Source Control URL: https://github.com/jwerak/automated_unicorn.git
- Execution Environment: *Default*

#### Create Job Template Unicorn/Sing

- Name: *Unicorn/Sing*
- Project: *Automated Unicorn*
- Playbook: *ansible/playbooks/play_music.yml*
- Inventory: None
- Extra Variables: e.g. `unicorn_api: http://malina4b.lan:5000`

**Add and Enable Survey**:

- Question: *Audio Title*
- Answer variable name: *unicorn_audio*
- Answer Type: *Multiple Choice (Single Select)*
- Options: ...

#### Create Job Template Unicorn/Color

- Name: *Unicorn/Color*
- Project: *Automated Unicorn*
- Playbook: *ansible/playbooks/change_color.yml*
- Inventory: None
- Extra Variables: e.g. `unicorn_api: http://malina4b.lan:5000`

**Add and Enable Survey**:

- Question: *Color*
- Answer variable name: *unicorn_color*
- Answer Type: *Multiple Choice (Single Select)*
- Options:
  - red
  - green
  - blue
