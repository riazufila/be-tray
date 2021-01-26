# be-tray (Early Development)


be-tray is a simple program that allows Linux services' status to be viewed from the system tray.


For a service to be shown on the tray, config/be-tray.json will need to be edited. For example, if the service mariadb wants to be monitored, then mariadb should be included in the config/be-tray.json as well as the path for active and inactive icons. For now, only a few services are included by default.


### In Progress
- [ ] Default icons for common services.
- [ ] Turn services on and off.
- [ ] View services' status realtime.
- [ ] etc.

### Done    
- [x] Parallel processes.
- [x] Read config file.
- [x] View active services.
