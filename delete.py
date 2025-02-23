#!/usr/bin/env python

import os
from vultr_dns import remove_record

remove_record(os.environ["CERTBOT_DOMAIN"],
                  os.environ["CERTBOT_VALIDATION"])
