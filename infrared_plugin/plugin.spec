plugin_type: other
subparsers:
    tripleo-clouds-inventory:
        description: Generate an inventory from the existing TripleO environment.
        include_groups: ["Ansible options", "Inventory", "Common options", "Answers file"]
        groups:
            - title: General Configuration
              options:
                local-python-interpreter:
                  type: Value
                  help: |
                    Localhost ansible python interpreter.
                  ansible_variable: 'local_ansible_python_interpreter'
                ir-workspace-update:
                  type: Flag
                  help: |
                    Update infrared workspace inventory using common role
                    'inventory-update'.
                    This is required in some scenarios.
                  ansible_variable: ir_workspace_update

            - title: Host variables
              options:
                  host:
                      type: Value
                      help: Hypervisor/Undercloud host name/ip
                      required: yes
                      ansible_variable: 'host'
                  user:
                      type: Value
                      help: SSH user to be used for the host connection
                      default: root
                      ansible_variable: 'user'
                  ssh-key:
                      type: Value
                      help: SSH key to be used for the host connection
                      default: ''
                      ansible_variable: 'ssh_key'
                  ssh-pass:
                      type: Value
                      help: |
                          SSH password to be used for the host connection.
                          When this option is used, dynamic ssh key will be generated and used.
                      default: ''
                      ansible_variable: 'ssh_pass'

            - title: Environment variables
              options:
                  setup-type:
                      type: Value
                      help: |
                          Define the type of the environment.
                          Possible values - virt, baremetal.
                          For virt or hybrid, use - virt.
                          For baremetal, use - baremetal
                      choices:
                          - 'virt'
                          - 'baremetal'
                      default: 'virt'
                      ansible_variable: 'setup_type'
                  overcloud-user:
                      type: Value
                      help: User used for connection to overcloud nodes
                      default: 'heat-admin'
                      ansible_variable: 'overcloud_user'
                  custom-undercloud-user:
                      type: Value
                      help: Define custom undercloud user of required
                      default: 'stack'
                      ansible_variable: 'custom_undercloud_user'
                  undercloud-groups:
                      type: Value
                      help: |
                          Define the groups, Undercloud host should be added to.
                          Multiple groups should be separated with comma.
                      default: 'undercloud,tester'
                      ansible_variable: 'undercloud_groups'
                  hypervisor-groups:
                      type: Value
                      help: |
                          Define the groups, Hypervisor host should be added to.
                          Multiple groups should be separated with comma.
                      default: 'hypervisor,shade'
                      ansible_variable: 'hypervisor_groups'
                  tenant-vms:
                      type: Bool
                      help: |
                          Whether to discover instances of a tenant.
                      default: 'false'
                      ansible_variable: 'tenant_vms'
                  tenant-rcfile:
                      type: Value
                      help: |
                         The path to the authentication file of the tenant
                      ansible_variable: tenant_rc_file_path
                  tenant-user:
                      type: Value
                      help: |
                         The SSH user to connect to the tenant VMs
                      ansible_variable: tenant_user
                  tenant-servers:
                      type: Value
                      help: |
                        Add to the inventory only the servers that match this filter
                      ansible_variable: tenant_servers
                  additional-groups:
                      type: NestedDict
                      action: append
                      help: |
                        Additional groups and the hosts to add to the inventory
                        Example: --additional-groups installer=undercloud-0,installer_host --additional-groups group2=host1
                      ansible_variable: additional_groups
                  undercloud-only:
                      type: Bool
                      help: |
                          Create inventory file with the underlcoud details only.
                          Could be used when overcloud nodes are unreachable.
                      default: 'false'
                      ansible_variable: 'undercloud_only'
                  venv-path:
                      type: Value
                      help: Virtual environment path
                      default: '/var/tmp/venv_shade'
                      ansible_variable: 'venv_path'
