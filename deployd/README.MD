## Directories


### manifests

This folder holds Enviroment Description Manifests (EDM) which are placed here by the WORKER API SERVICE. **Important:** do not place other files here.

```yaml
provider: virtualbox
name: vm1
# actions: start|stop|reset|delete
# action: 'delete'

specs:
  cpus: 1
  memory: 512
  # Port forwarding
  ports:
    - name: rule1
      type: tcp
      hostPort: 2224
      guestPort: 22
```

### ports

Holds the ports allocated for each virtual machine. An example of the content of this folder is shown bellow. **Important:** do not place other files here.

```sh
vm1/
    2221.txt
    2222.txt
vm2/
    2224.txt
...
```

### resources

Holds the .vdi templates used to deploy virtual machines. An example of the content of this folder is shown bellow.

```sh
base.vdi
...
```

### virtualbox 

Holds Python interfaces to interact with the VirtualBox hypervisor. Additionally, holds automated deployment interfaces for virtual machines.