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

## Setup

### Execution node setup

Download installation bundle as [described in the documentation](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/installing_on_openshift_container_platform/operator-add-execution-nodes_operator-platform-doc#operator-add-execution-nodes_operator-platform-doc).

Setup the Execution node:

```bash

```

### Automation Controller setup

#### Create Project

- Name: *Automated Unicorn*
- Source Control Type: *Git*
- Source Control URL: https://github.com/jwerak/automated_unicorn.git
- Execution Environment: *Default*

#### Create Job Template

- Name: *Unicorn/Sing*
- Project: *Automated Unicorn*
- Playbook: *ansible/playbooks/play_music.yml*
- Inventory: Demo Inventory
- Extra Variables: e.g. `unicorn_api: http://malina4b.lan:5000`

**Add and Enable Survey**:

- Question: *Audio Title*
- Answer variable name: *unicorn_api*
- Answer Type: *Multiple Choice (Single Select)*
- Options: ...
