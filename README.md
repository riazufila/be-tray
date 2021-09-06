# be-tray

be-tray is a simple program that allows Linux services' status to be viewed from the system tray.

# How to Use?

**_Important: Requires Linux machine with systemd!_**

1. Install PyQt5 with `pip` or use you preferred package manager.

```sh
pip install PyQt5
```

2. Then, edit `be-tray.conf` to include whatever service you wish to display.

3. Add icons in `icons/` and edit `be-tray.conf` accordingly.

4. Execute be-tray. Then, according to the services stated in `be-tray.conf`, the icons should display accordingly.
