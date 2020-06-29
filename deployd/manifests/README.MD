# Enviroment Description Manifest

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