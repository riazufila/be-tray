# be-tray (Early Development)


be-tray is a simple program that allows Linux services' status to be viewed from the system tray.


For a service to be shown on the tray, config/be-tray.json will need to be edited. E.g., to monitor mariadb, mariadb should be included in the config/be-tray.json as well as the path for active and inactive icons. For now, only a few services are included by default.


# Quick Start


Install PyQt5:

```
pip install PyQt5
```
Or use your preferred package manager.


Then, edit `config/be-tray.json` to include whatever service you wish to display.


be-tray uses systemd to check for active and inactive services. Hence, only systems that uses systemd to manage services are supported.


### In Progress
- [ ] Default icons for common services.
- [ ] Turn services on and off.
- [ ] Basic logic algorithms.
- [ ] etc.

### Done    
- [x] Parallel processes.
- [x] Read config file.
- [x] View active services.
- [x] View services' status realtime.
