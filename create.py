#!/usr/bin/env python

import os
from vultr_dns import create_record

create_record(os.environ["CERTBOT_DOMAIN"],
                  os.environ["CERTBOT_VALIDATION"])