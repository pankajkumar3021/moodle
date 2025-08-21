# Moodle

<p align="center"><a href="https://moodle.org" target="_blank" title="Moodle Website">
  <img src="https://raw.githubusercontent.com/moodle/moodle/main/.github/moodlelogo.svg" alt="The Moodle Logo">
</a></p>

[Moodle][1] is the World's Open Source Learning Platform, widely used around the world by countless universities, schools, companies, and all manner of organisations and individuals.

Moodle is designed to allow educators, administrators and learners to create personalised learning environments with a single robust, secure and integrated system.

## Documentation

- Read our [User documentation][3]
- Discover our [developer documentation][5]
- Take a look at our [demo site][4]

## Community

[moodle.org][1] is the central hub for the Moodle Community, with spaces for educators, administrators and developers to meet and work together.

You may also be interested in:

- attending a [Moodle Moot][6]
- our regular series of [developer meetings][7]
- the [Moodle User Association][8]

## Installation and hosting

Moodle is Free, and Open Source software. You can easily [download Moodle][9] and run it on your own web server, however you may prefer to work with one of our experienced [Moodle Partners][10].

Moodle also offers hosting through both [MoodleCloud][11], and our [partner network][10].

## License

Moodle is provided freely as open source software, under version 3 of the GNU General Public License. For more information on our license see

[1]: https://moodle.org
[2]: https://moodle.com
[3]: https://docs.moodle.org/
[4]: https://sandbox.moodledemo.net/
[5]: https://moodledev.io
[6]: https://moodle.com/events/mootglobal/
[7]: https://moodledev.io/general/community/meetings
[8]: https://moodleassociation.org/
[9]: https://download.moodle.org
[10]: https://moodle.com/partners
[11]: https://moodle.com/cloud
[12]: https://moodledev.io/general/license

 Moodle documentation for installing on Debian is not correct . We need to refer to this document [Moodle additional steps ](https://docs.moodle.org/401/en/Step-by-step_Install_Guide_for_Debian )

# Step 1 LAMP server installaton  

#Update the system and install git, Apache, PHP and modules required by Moodle
sudo apt-get update  
sudo apt-get install -y apache2 php8.3 libapache2-mod-php8.3 php8.3-mysql graphviz aspell git   
sudo apt-get install -y clamav php8.3-pspell php8.3-curl php8.3-gd php8.3-intl php8.3-mysql ghostscript  
sudo apt-get install -y php8.3-xml php8.3-xmlrpc php8.3-ldap php8.3-zip php8.3-soap php8.3-mbstring  


#Install Debian default database MariaDB  
sudo apt-get install -y mariadb-server mariadb-client  
echo "Step 1 has completed."  


# Step 2 Clone the Moodle repository into /opt and copy to /var/www
# Use MOODLE_401_STABLE branch as Debian 11 ships with php8.3
echo "Cloning Moodle repository into /opt and copying to /var/www/"  
echo "Be patient, this can take several minutes."  
cd /var/www  
sudo git clone https://github.com/moodle/moodle.git  
cd moodle  
sudo git checkout -t origin/MOODLE_500_STABLE  
echo "Step 2 has completed."  


# Step 3 Directories, ownership, permissions, php.ini changes and virtual hosts 
sudo mkdir -p /var/www/moodledata  
sudo chown -R www-data /var/www/moodledata  
sudo chmod -R 777 /var/www/moodledata  
sudo chmod -R 755 /var/www/moodle  
# Change the Apache DocumentRoot using sed so Moodle opens at http://webaddress  
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/moodle.conf  
sudo sed -i 's|/var/www/html|/var/www/moodle|g' /etc/apache2/sites-available/moodle.conf  
sudo a2dissite 000-default.conf  
sudo a2ensite moodle.conf  
sudo systemctl reload apache2  
# Update the php.ini files, required to pass Moodle install check  
sudo sed -i 's/.*max_input_vars =.*/max_input_vars = 5000/' /etc/php/8.3/apache2/php.ini  
sudo sed -i 's/.*post_max_size =.*/post_max_size = 80M/' /etc/php/8.3/apache2/php.ini  
sudo sed -i 's/.*upload_max_filesize =.*/upload_max_filesize = 80M/' /etc/php/8.3/apache2/php.ini  
# Restart Apache to allow changes to take place  
sudo service apache2 restart  
echo "Step 3 has completed."  


# Step 4 Set up cron job to run every minute  
echo "Cron job added for the www-data user."  
CRON_JOB="* * * * * /var/www/moodle/admin/cli/cron.php >/dev/null"  
echo "$CRON_JOB" > /tmp/moodle_cron  
sudo crontab -u www-data /tmp/moodle_cron  
sudo rm /tmp/moodle_cron  
echo "Step 4 has completed."  

# Step 5 Secure the MySQL service and create the database and user for Moodle  
MYSQL_ROOT_PASSWORD=$(openssl rand -base64 6)  
MYSQL_MOODLEUSER_PASSWORD=$(openssl rand -base64 6)  
# Set the root password using mysqladmin  
sudo mysqladmin -u root password "$MYSQL_ROOT_PASSWORD"  
# Create the Moodle database and user  
echo "Creating the Moodle database and user..."  
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF  
CREATE DATABASE moodle DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
CREATE USER 'moodleuser'@'localhost' IDENTIFIED BY '$MYSQL_MOODLEUSER_PASSWORD';  
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, CREATE TEMPORARY TABLES, DROP, INDEX, ALTER ON moodle.* TO 'moodleuser'@'localhost';  
FLUSH PRIVILEGES;  
\q  
EOF  
# Display the generated passwords (if needed, for reference)  
echo "SQL root password: $MYSQL_ROOT_PASSWORD, moodle SQL password: $MYSQL_MOODLEUSER_PASSWORD"  
sudo chmod -R 777 /var/www/moodle  
echo "Step 5 has completed."  
