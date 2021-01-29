# be-tray (Early Development)


- be-tray is a simple program that allows Linux services' status to be viewed from the system tray.


- **be-tray uses systemd** to check for active and inactive services. Hence, only systems that uses systemd to manage services are supported.


# Quick Start


- Install PyQt5:

```sh
pip install PyQt5
```

Or use your preferred package manager.


- Then, edit `config/be-tray.json` to include whatever service you wish to display. Icons should be placed in `icons/` and the format for icon paths in `config/be-tray.json` should be as follows.

```json
{
    "ufw": [
        "../icons/shield-on.png",
        "../icons/shield-off.png"
    ],
    "httpd": [
        "../icons/web-on.png",
        "../icons/web-off.png"
    ]
}
```


# TODO


### In Progress
- [ ] Default icons for common services.
- [ ] etc.

### Done    
- [x] Parallel processes.
- [x] Read config file.
- [x] View active services.
- [x] View services' status realtime.
