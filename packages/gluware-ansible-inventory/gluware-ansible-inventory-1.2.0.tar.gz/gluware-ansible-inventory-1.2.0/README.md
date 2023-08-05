# Gluware Ansible Inventory (Inventory plugin and Gluware Ansible modules)

This python package installs a Ansible Inventory plugin (glu_devices) to interact with a Gluware Control system to get the current network devices of a organization.  A "inventory" user can be created in the Gluware Control system that can then be used in the configuration of the glu_devices inventory plugin to access the devices of the Gluware Control system.  

The glu_devices Ansible Inventory plugin gives Ansible playbooks the ability to connect to Gluware devices and get the "ansible_network_os" property of the device to know what kind of device it is (if the discovery function in Gluware is used).  The glu_devices inventory plugin also exposes to Ansible playbooks any custom Gluware device attributes that start with "ansible_var_" (minus the "ansible_var_" part) to act on within the logic of the playbook.  In addition, the other Gluware device attributes can be mapped to Ansible variables through configuration settings of the glu_devices.

In version 1.2, Gluware Ansible modules are also installed to allow interaction with Gluware device data from within playbook tasks. The Inventory plugin was updated to supply the 'glu_device_id' for the Gluware Ansible modules. The modules are identified as follows:
* glu_audit_config
    * Perform a audit on the current captured config on a Gluware Device
* glu_capture_config
    * Perform a capture config on a Gluware Device
* glu_run_discover_device_attributes
    * Perform a discover device attributes on a Gluware Device
* glu_update_device_attributes
    * Update device attributes on a Gluware Device

To install on the system that is running Ansible run the command line: "pip install gluware-ansible-inventory".  If updating to a later version the run the command line: "pip install -I gluware-ansible-inventory".

After install run the command line: "ansible-doc -t inventory glu_devices" to see the specifics of how to use the glu_devices inventory plugin to connect to the Gluware Control system.  To see the documentation for each module run the command line: "ansible-doc -t module {{ module_name }}".

* Install Command 
    * $ pip install gluware-ansible-inventory
* Update Command: 
    * $ pip install -I gluware-ansible-inventory
* Usage documentation command after install
    * $ ansible-doc -t inventory glu_devices
    * $ ansible-doc -t module glu_audit_config
    * $ ansible-doc -t module glu_capture_config
    * $ ansible-doc -t module glu_run_discover_device_attributes
    * $ ansible-doc -t module glu_update_device_attributes

* Installation imlementation note:
    * The 'pip install gluware-ansible-inventory' places the 'glu_devices.py' file in the '/usr/share/ansible/plugins/inventory/' directory for ansible to find the glu_devices inventory plugin.  The modules are placed in the '/usr/share/ansible/plugins/modules/'
    directory for ansible to find the Gluware modules.
    * The inventory plugin is just the 'glu_devices.py' file with no other files being used.

