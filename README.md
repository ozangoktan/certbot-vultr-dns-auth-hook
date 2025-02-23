# certbot-vultr-dns-auth-hook

This is an "auth hook" for Certbot that enables you to perform DNS-01 authorization via Vultr's DNS service. It has been forked to make it nicer to use with certbot in a docker container.

All it requires is that you have your [Vultr API key](https://my.vultr.com/settings/#settingsapi), and that you have set your domain up [as a zone in Vultr](https://my.vultr.com/dns/).

## Usage

1. Clone the repository to **\{hook-directory\}**
2. Set environment variable **VULTR_API_KEY** and optionally **VULTR_BIND_DELAY** which defaults to 30 seconds of delay.
3. Point certbot to use it by passing in parameters `--manual-auth-hook {hook-directory}/create.py --manual-cleanup-hook {hook-directory}/delete.py` 
