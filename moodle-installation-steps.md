# 📘 Moodle Installation on Debian (Apache, MySQL/MariaDB, PHP 8.3)

This repository documents the commands and steps required to install and configure **Moodle** on a Debian server with **Apache**, **MySQL/MariaDB**, and **PHP 8.3**, along with applying the **Adaptable** theme.

---

## 🔧 Prerequisites
- Debian 12 (Bookworm) or newer  
- Root or sudo privileges  
- Internet connectivity  

---

## 📥 Step 1: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🌐 Step 2: Install Apache
```bash
sudo apt install apache2 -y
sudo systemctl enable apache2
sudo systemctl start apache2
```

---

## 🗄️ Step 3: Install MySQL/MariaDB
```bash
sudo apt install mariadb-server mariadb-client -y
sudo systemctl enable mariadb
sudo systemctl start mariadb
```

Secure the installation:
```bash
sudo mysql_secure_installation
```

---

## 💻 Step 4: Install PHP 8.3 and Required Extensions
Enable **Sury PHP repository**:
```bash
sudo apt install -y ca-certificates apt-transport-https lsb-release wget
sudo wget https://packages.sury.org/php/apt.gpg -O /etc/apt/trusted.gpg.d/php.gpg
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list
sudo apt update
```

Install PHP 8.3 + Moodle dependencies:
```bash
sudo apt install -y php8.3 php8.3-cli php8.3-common php8.3-mysql php8.3-xml php8.3-xmlrpc php8.3-curl php8.3-gd php8.3-intl php8.3-zip php8.3-mbstring php8.3-soap php8.3-bcmath php8.3-ldap libapache2-mod-php8.3 unzip git
```

Verify versions:
```bash
apache2 -v
php -v
mysql -V
```

---

## 🗄️ Step 5: Create Moodle Database
```bash
sudo mysql
```

Inside MySQL:
```sql
CREATE DATABASE moodle DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'moodleuser'@'localhost' IDENTIFIED BY 'YourStrongPassword';
GRANT ALL PRIVILEGES ON moodle.* TO 'moodleuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 📂 Step 6: Deploy Moodle
Clone Moodle into Apache root:
```bash
cd /var/www/html
sudo git clone -b MOODLE_404_STABLE git://git.moodle.org/moodle.git moodle
```

Create Moodle data directory:
```bash
sudo mkdir -p /var/moodledata
sudo chown -R www-data:www-data /var/moodledata
sudo chmod -R 770 /var/moodledata
```

Set permissions:
```bash
sudo chown -R www-data:www-data /var/www/html/moodle
sudo chmod -R 755 /var/www/html/moodle
```

---

## 🌍 Step 7: Configure Apache
Create virtual host:
```bash
sudo nano /etc/apache2/sites-available/moodle.conf
```

Add:
```apache
<VirtualHost *:80>
    ServerAdmin admin@example.com
    DocumentRoot /var/www/html/moodle
    ServerName your-domain.com
    ServerAlias www.your-domain.com

    <Directory /var/www/html/moodle>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/moodle_error.log
    CustomLog ${APACHE_LOG_DIR}/moodle_access.log combined
</VirtualHost>
```

Enable site + modules:
```bash
sudo a2ensite moodle.conf
sudo a2enmod rewrite
sudo systemctl reload apache2
```

---

## 👤 Step 8: Moodle CLI Administration

Create admin user:
```bash
sudo -u www-data php ./admin/cli/create_user.php   --username=admin   --password=0netw0three   --email=pankajkumar.3021@gmail.com   --firstname=Site   --lastname=Administrator
```

Reset password:
```bash
sudo -u www-data php ./admin/cli/reset_password.php   --username=admin   --password=0netw0three   --ignore-password-policy
```

Assign administrator role:
```bash
sudo -u www-data php ./admin/cli/assign_role.php   --role=1   --user=admin   --contextlevel=10
```

---

## ⏰ Step 9: Cron Setup
Moodle requires cron for background tasks:
```bash
sudo crontab -u www-data /tmp/moodle_cron
sudo rm /tmp/moodle_cron
```

---

## 🚀 Step 10: Non-Interactive CLI Install (Optional)
```bash
sudo -u www-data /usr/bin/php /var/www/html/moodle/admin/cli/install.php   --non-interactive   --lang=en   --wwwroot="$PROTOCOL$WEBSITE_ADDRESS"   --dataroot=/var/www/moodledata   --dbtype=mariadb   --dbhost=localhost   --dbname=moodle   --dbuser=moodleuser   --dbpass="$MYSQL_MOODLEUSER_PASSWORD"   --fullname="Generic Moodle"   --shortname="GM"   --adminuser=admin   --adminpass="$MOODLE_ADMIN_PASSWORD"   --adminemail=pankajkumar.3021@gmail.com   --agree-license
```

---

## 🎨 Step 11: Install and Apply Adaptable Theme

### 1. Download Adaptable
```bash
cd /var/www/html/moodle/theme

sudo wget https://moodle.org/plugins/download.php/37066/theme_adaptable_moodle50_2025040804.zip
sudo unzip theme_adaptable_moodle50_20250408040804.zip
sudo chown -R www-data:www-data adaptable/
sudo -u www-data php /var/www/html/moodle/admin/cli/cfg.php --name=theme --set=adaptable

sudo git checkout MOODLE_404_STABLE
cd ..
```

### 2. Fix Permissions
```bash
sudo chown -R www-data:www-data /var/www/html/moodle/theme/adaptable
sudo chmod -R 755 /var/www/html/moodle/theme/adaptable
```

### 3. Purge Cache
```bash
sudo -u www-data php /var/www/html/moodle/admin/cli/purge_caches.php
```

### 4. Set Adaptable as Default Theme
```bash
sudo -u www-data php /var/www/html/moodle/admin/cli/cfg.php --name=theme --set=adaptable
```

### 5. Verify in Browser
Open Moodle in your browser and confirm **Adaptable** is applied.  
Further customization:  
`Site administration → Appearance → Themes → Adaptable`
### 6. Moodle Safety measures
1. Moodle Code Directory (/var/www/html/moodle)

This contains Moodle’s PHP code.

The web server (www-data) should only read it, not modify it.

Ownership:

sudo chown -R root:root /var/www/html/moodle


Permissions:

sudo find /var/www/html/moodle -type f -exec chmod 644 {} \;
sudo find /var/www/html/moodle -type d -exec chmod 755 {} \;


Exception: The moodledata folder (see below).

👉 This ensures your server can run the code but attackers (or even Moodle itself) cannot overwrite files if there’s a security flaw.

2. Moodle Data Directory (/var/moodledata)

This is where Moodle stores cache, sessions, uploaded files, temp files.

It must be writable by the web server (www-data).

Ownership:

sudo chown -R www-data:www-data /var/moodledata


Permissions:

sudo find /var/moodledata -type f -exec chmod 664 {} \;
sudo find /var/moodledata -type d -exec chmod 775 {} \;


⚡ Security Note: Never put moodledata inside /var/www/html/ (the web root) — it should always be outside web-accessible directories.

3. Extra Security Hardening

Disable direct access to config.php:

sudo chmod 640 /var/www/html/moodle/config.php


Prevent web access to .git, .env, or hidden files with Apache/Nginx rules.

Regularly update Moodle and dependencies.

✅ In short:

/var/www/html/moodle → read-only for web server (owned by root:root).

/var/moodledata → writable by web server (owned by www-data).
---

## ✅ Access Moodle
Once installation completes, open:
```
http://your-server-ip-or-domain
```

---

✍️ Maintained by: *Your Name*  
📧 Contact: *your-email@example.com*  
