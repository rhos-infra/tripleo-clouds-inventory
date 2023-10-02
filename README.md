# TripleO Clouds Inventory

## Description
TripleO Clouds Inventory play will generate a new inventory file from the provided Undercloud/Hypervisor host on the existing deployment.

From time to time, we may get an already installed Openstack environment for work/testing/etc.
In order to be able to run an Ansible playbooks or different ad-hoc commands against the overcloud nodes,
inventory file is required.

The role could be used as a standalone role or infrared plugin.

## Caveats

**This plugin/playbook doesn't support the native [openstack.cloud](https://galaxy.ansible.com/ui/repo/published/openstack/cloud/) collection.**

**Tested on `ansible <= 2.9.27`.**

## Structure
At the end of the play the following structure will appear:
```
|-> inventory file (soft link to the last environment)
|-> ansible.ssh.config (soft link to the last environment)
|
|-> environments
    |
    |-> First environment
    |     |-> inventory file
    |     |-> ansible.ssh.config file
    |     |-> ssh keys
    |
    |-> Second environment
    |     |-> inventory file
    |     |-> ansible.ssh.config file
    |     |-> ssh keys
```
**Note!** - Each run, the latest generated environment will be symlink to the **inventory** and **ansible.ssh.config** at the root of the ansible repo directory.

## Supported environment types:
The play adapted to the baremetal, hybrid or virt environment.  
**Baremetal** - Undercloud and Overcloud nodes (Controllers, Computes, etc...) are fully baremetal.  
**Hybrid** - Undercloud and Controllers nodes are virtual (Resides on a single host) and the Computes are baremetal.  
**Virt** - Undercloud and Overcloud nodes (Controllers, Computes, etc...) are virtual and resides on a single machine.

**Note!** - For baremetal environment add ```-e setup_type=baremetal```, and for virt or hybrid environment add ```-e setup_type=virt```

The play could be run in two available scenarios:
1. The public key of your ssh key already located on the Undercloud/Hypervisor host.  
   The play will generate three files:
  * inventory
  * ansible.ssh.config
  * id_rsa_overcloud

2. You have only the password of the Undercloud/Hypervisor host.  
   The play will generate five files:
  * inventory
  * ansible.ssh.config
  * id_rsa_overcloud
  * id_rsa_undercloud
  * id_rsa_undercloud.pub

Inventory - Will hold the Undercloud node and all Overcloud nodes located within the environment.  
Ansible.ssh.config - SSH config file. Allow to connect to the overcloud nodes from the localhost.
```
For example:
ssh -F ansible.ssh.config controller-0
```
Id_rsa_overcloud - The ssh key for the connection to overcloud nodes. Used by the above files.  
Id_rsa_undercloud - In case, password provided to Undercloud host, play will generate new ssh key  
                    and will use it for the connection to Undercloud host.  
Id_rsa_undercloud.pub - Public key of the id_rsa_undercloud.

***
## Play variables

Path to python executable on localhost that will execute ansible modules.  
Default: '/usr/bin/python'
```
local-python-interpreter: "$(which python"
```

Perform infrared inventory workspace update using infrared inventory-update role.
Default: 'False'
```
ir-workspace-update
```

Provide the type of the environment.  
Default: 'virt'  
Mandatory variable.
```
setup_type
```

Provide the undercloud host.  
Mandatory variable.
```
host
```

Provide the user for the hypervisor/undercloud.  
Default user:
- 'root' for virt or hybrid
- 'stack' for baremetal
Not mandatory variable.
```
user: stack
```

Specify the Undercloud ssh private key file.  
The public key should already be copied to the undercloud host.  
One of two parameters should be provided: ssh_key or ssh_pass.
```
ssh_key
```

Specify the password for the Undercloud host.  
Use this variable in case there is no your public key on the Undercloud host.  
When 'ssh_pass' is used, custom ssh key will be generated.  
One of two parameters should be provided: ssh_key or ssh_pass.
```
ssh_pass
```

Overcloud user. The user which has an access to the overcloud nodes.  
Default: 'heat-admin'.
```
overcloud_user: heat-admin
```

RC file path.  
Default: '/home/stack/stackrc'.
```
rc_file_path
```

Define custom undercloud user if required.  
By default the variable is not used.  
Default value is - stack.
```
custom_undercloud_user
```

Undercloud could be used for various tasks like tester or something else.  
The tasks could use inventory groups.  
Define the groups, Undercloud host should be added to.  
Multiple groups should be separated by the comma.
```
undercloud_groups: undercloud,tester
```

If true, create an inventory file for the undercloud environment only.  
Default value is set to - false
```
undercloud_only: true
```

If true, Discover the VMs of the tenant  
```
tenant_vms: false
```

When tenant_vms is true, Add to the inventory only VMs which their names match the *tenant_servers* filter
```
tenant_servers: 'installer*'
```

The path to the authentication file of the tenant (**tenant_vms** must be **true**)  
```
tenant_rc_file_path
```

The SSH user to connect to the tenant VMs ((**tenant_vms** must be **true**)
```
tenant-user
```

Add addiotional groups to the inventory  
In the following example: Add the installer_host to the installer group  
```
additional_groups:
  installer:
    - installer_host
```
***
## Examples
The example of running the TripleO Clouds Inventory playbook.  
With SSH key file for baremetal environment:
```
ansible-playbook tripleo_clouds_inventory.ymltripleo_clouds_inventory.yml -e host=undercloud-host-fqdn/ip -e ssh_key=/path/to/ssh/private/file -e setup_type=baremetal
```
With SSH key file for hybrid or virt environment:
```
ansible-playbook tripleo_clouds_inventory.yml -e host=undercloud-host-fqdn/ip -e user=root -e ssh_key=/path/to/ssh/private/file -e setup_type=virt
```

With password:
```
ansible-playbook tripleo_clouds_inventory.yml -e host=undercloud-host-fqdn/ip -e user=root -e ssh_pass=undercloud_password
```
