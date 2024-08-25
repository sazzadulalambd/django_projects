To stop and start the firewall using `firewalld`, you can use the following commands:

### **Stop `firewalld` Service**
Stopping the firewall will disable it, which could expose your server to security risks. Use this only for troubleshooting purposes and ensure you have alternative protection measures in place.

```bash
sudo systemctl stop firewalld
```

### **Start `firewalld` Service**
To start the firewall again after stopping it:

```bash
sudo systemctl start firewalld
```

### **Check Firewall Status**
To verify that `firewalld` is running:

```bash
sudo systemctl status firewalld
```

### **Restart `firewalld` Service**
To restart the firewall:

```bash
sudo systemctl restart firewalld
```

### **Verify Firewall Rules**
After restarting, ensure your firewall rules are correctly set:

```bash
sudo firewall-cmd --list-all
```

### **Additional Commands**
- **Enable `firewalld` to start on boot**:
  ```bash
  sudo systemctl enable firewalld
  ```

- **Disable `firewalld` from starting on boot**:
  ```bash
  sudo systemctl disable firewalld
  ```

Stopping the firewall temporarily can help determine if it is causing connectivity issues. However, be sure to re-enable and configure it properly to maintain the security of your server.

If you are still having issues accessing phpMyAdmin from outside your network, and the firewall isn’t the problem, you may need to check other aspects of your server configuration or network settings.
