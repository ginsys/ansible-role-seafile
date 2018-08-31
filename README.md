ansible-role-seafile
====================

An ansible role to deploy Seafile, an Open Source Cloud Storage. http://seafile.com/


Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.


Role Variables
--------------

Role variables are well documented in defaults/main.yml
Some constants are set in vars/main.yml too, you normally do not want to change those, as they might affect how the
role behaves, in unsuspected ways.


Dependencies
------------

N/A


Version tags
------------

Version tags (at least starting from 4.0) follow this scheme X.Y.Z scheme:

X.Y points to the major.minor upstream version of seafile, this role supports, or was
at least tested with.

Z points to bugfix updates to this role itself, and does not depend on any bugfix
release from upstream or any upstream version change.


Example Playbook
----------------

Using `group_vars/seafile.yml`:
(beware, this is just an old example!)

```
---
# names, files and directory locations
seafile_user:               seafile
seafile_user_home:          /home/seafile
seafile_org_name:           Ginsys
seafile_server_name:        '{{ seafile_org_name }}'
seafile_ip_or_domain:       files.ginsys.eu
seafile_service_url:        https://{{ seafile_ip_or_domain }}
seafile_custom_files_path:  files/seafile/custom/

seafile_quota_enable:       false
seafile_quota_default:      2

seafile_history_keepall:    false
seafile_history_keep_days:  30

seafile_max_upload_size_enable:         false # set to true to enable max
seafile_max_upload_size:                200  # MB
seafile_max_download_dir_size_enable:   false # set to true to enable max
seafile_max_download_dir_size:          200  # MB

seafile_email_enable:       enable
seafile_email_use_tls:      false
seafile_email_host:         '{{ relayservers[0] }}'
seafile_email_user:         '{{ seafile_seahub_admin_email }}'
seafile_email_password:     ''
seafile_email_port:         25
seafile_default_from_email: '{{ seafile_email_user }}'
seafile_server_email:       '{{ seafile_email_user }}'

seafile_time_zone:  'Europe/Brussels'
seafile_site_base:  'http://{{ seafile_ip_or_domain }}/'
seafile_site_name:  '{{ seafile_org_name }}' # used in email notifications
seafile_site_title: '{{ seafile_org_name }}'
seafile_site_root:  '/'
seafile_cloud_mode: true
seafile_logo_path:  'custom/ginsys_seafile_logo.png'
seafile_css_path:   'custom/ginsys_seafile.css'
seafile_allowed_hosts: "['.ginsys.eu']"

# webdav settings
seafile_webdav_enabled:     true
seafile_webdav_fastcgi:     true

# seahub settings
seafile_seahub_admin_email: hostmaster@ginsys.eu

# database settings
seafile_backend:            'mysql'
seafile_db_user:            'seafile'

# cron jobs
seafile_cron_gc_enabled:    true


# mysql configuration
#
mysql_bind_address:         '{{ seafile_db_host }}'
mysql_db:
- name:                     '{{ seafile_db_name.ccnet }}'
  replicate:                no
- name:                     '{{ seafile_db_name.seafile }}'
  replicate:                no
- name:                     '{{ seafile_db_name.seahub }}'
  replicate:                no
mysql_users:
- name:                     '{{ seafile_db_user }}'
  pass:                     '{{ seafile_db_pass }}'
  priv: >
    {{ seafile_db_name.ccnet    ~ ".*:ALL/" ~
       seafile_db_name.seafile  ~ ".*:ALL/" ~
       seafile_db_name.seahub   ~ ".*:ALL"  }}

# nginx configuration
#
nginx_max_clients:          128
nginx_http_params:
  sendfile:                 "on"
  tcp_nopush:               "on"
  tcp_nodelay:              "on"
  keepalive_timeout:        "65"
  access_log:               "/var/log/nginx/access.log"
  error_log:                "/var/log/nginx/error.log"
  types_hash_max_size:      2048
  server_names_hash_bucket_size: 64

nginx_sites:
 - server:
    file_name:      '{{ seafile_ip_or_domain }}'
    server_name:    '{{ seafile_ip_or_domain }}'
    listen:         '[::]:80 ipv6only=off'
    rewrite:        ^ https://$http_host$request_uri? permanent
 - server:
    file_name:      '{{ seafile_ip_or_domain }}-ssl'
    server_name:    '{{ seafile_ip_or_domain }}'
    listen:         '[::]:443 ipv6only=off'
    proxy_set_header: 'X-Forwarded-For $remote_addr'
    # https://mozilla.github.io/server-side-tls/ssl-config-generator/
    ssl:            "on"
    ssl_certificate_key:    /etc/ssl/private/ginsys.eu.key.pem
    ssl_certificate:        /etc/ssl/private/ginsys.eu.crt.pem
    ssl_session_timeout:    1d
    # Diffie-Hellman parameter for DHE ciphersuites, recommended 2048 bits
    ssl_dhparam:            /etc/ssl/private/dh4096.pem
    # intermediate configuration. tweak to your needs.
    ssl_protocols:          "TLSv1 TLSv1.1 TLSv1.2"
    ssl_prefer_server_ciphers: 'on'
    ssl_ciphers: "'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA'"
    # HSTS (ngx_http_headers_module is required) (15768000 seconds = 6 months)
    #add_header: "Strict-Transport-Security max-age=15768000"
    # OCSP Stapling ---
    # fetch OCSP records from URL in ssl_certificate and cache them
    ssl_stapling: "on"
    ssl_stapling_verify: "on"
    ## verify chain of trust of OCSP response using Root CA and Intermediate
    ## certs
    #ssl_trusted_certificate /path/to/root_CA_cert_plus_intermediates;
    #resolver <IP DNS resolver>;


   location:
   ##
   ## WARNING ##
   ## recent seafile versions do not support fastcgi any more !
   ##
    - name:  /
      fastcgi_pass:  127.0.0.1:{{ seafile_fastcgi_port }}
      "fastcgi_param SCRIPT_FILENAME":     $document_root$fastcgi_script_name
      "fastcgi_param PATH_INFO":           $fastcgi_script_name
      "fastcgi_param SERVER_PROTOCOL":     $server_protocol
      "fastcgi_param QUERY_STRING":        $query_string
      "fastcgi_param REQUEST_METHOD":      $request_method
      "fastcgi_param CONTENT_TYPE":        $content_type
      "fastcgi_param CONTENT_LENGTH":      $content_length
      "fastcgi_param SERVER_ADDR":         $server_addr
      "fastcgi_param SERVER_PORT":         $server_port
      "fastcgi_param SERVER_NAME":         $server_name
      "fastcgi_param HTTPS":               on
      "fastcgi_param HTTP_SCHEME":         https
      access_log:    /var/log/nginx/seahub.access.log
      error_log:     /var/log/nginx/seahub.error.log
    - name: /seafhttp
      rewrite:               ^/seafhttp(.*)$ $1 break
      proxy_pass:            http://127.0.0.1:{{ seafile_httpserver_port }}
      client_max_body_size:  0
      access_log:    /var/log/nginx/seafhttp.access.log
      error_log:     /var/log/nginx/seafhttp.error.log
    - name: /media
      root: '{{ seafile_latest_dir }}/seahub/'
      access_log:    /var/log/nginx/media.access.log
      error_log:     /var/log/nginx/media.error.log
    - name:  '{{ seafile_webdav_path }}'
      fastcgi_pass:  127.0.0.1:{{ seafile_webdav_port }}
      "fastcgi_param SCRIPT_FILENAME":     $document_root$fastcgi_script_name
      "fastcgi_param PATH_INFO":           $fastcgi_script_name
      "fastcgi_param SERVER_PROTOCOL":     $server_protocol
      "fastcgi_param QUERY_STRING":        $query_string
      "fastcgi_param REQUEST_METHOD":      $request_method
      "fastcgi_param CONTENT_TYPE":        $content_type
      "fastcgi_param CONTENT_LENGTH":      $content_length
      "fastcgi_param SERVER_ADDR":         $server_addr
      "fastcgi_param SERVER_PORT":         $server_port
      "fastcgi_param SERVER_NAME":         $server_name
      "fastcgi_param HTTPS":               on
      "fastcgi_param HTTP_SCHEME":         https
      client_max_body_size:                50m
      access_log:    /var/log/nginx/seafdav.access.log
      error_log:     /var/log/nginx/seafdav.error.log

# ufw firewall
# https://github.com/haiwen/seafile/wiki/Firewall-settings-for-seafile-server
firewall_allowed_services:
  - OpenSSH
firewall_allowed_ports:
  - port:   80
    proto:  tcp
  - port:   443
    proto:  tcp
```

Run this playbook:

```
- hosts:        seafile
  sudo:         true
  gather_facts: true


###########
#
  pre_tasks:
  - name:       provision ssl dir
    file:
      dest:     /etc/ssl/private
      state:    directory
      owner:    root
      group:    ssl-cert
      mode:     0750
    tags:       ssl

  - name:       copy ssl certificates
    copy:
      src:      files/ssl/{{ item }}
      dest:     /etc/ssl/private/{{ item }}
      owner:    root
      group:    ssl-cert
      mode:     0640
    with_items:
    - ginsys.eu.key.pem
    - ginsys.eu.crt.pem
    - dh4096.pem
    tags:       ssl

###########
#
  roles:

    - role:     rackufw
      tags:
                - firewall
                - ufw

    - role:     Ginsys.mysql
      tags:     mysql

    - role:     Ginsys.seafile
      tags:     seafile

    - role:     Ginsys.nginx
      tags:     nginx


###########
#
  post_tasks:
  - name:       allow web server access to seafile data
    user:
      name:     'www-data'
      groups:   '{{ seafile_user }}'
      append:   yes
    tags:
                - seafile
                - seafile_custom

```


License
-------

GNU General Public License v3.0


Author Information
------------------

Serge van Ginderachter and contributors
