#settings

import os
import sys

# filters available on this configuration
import multiprocessing
from ipaddress import ip_network
from aes.conf.default_settings import SERVICES

DEBUG = False

SERVICES = {
    'http': {
        'class': 'aes.services.HttpService',
        'port': 8000,
        'host': '0.0.0.0'
    },
    'inbound': {
        'class': 'aes.services.InboundSMTPService',
        'host': '0.0.0.0',
        'port': 1025,
        'ssl': None,
        'starttls': {
            'cert': '/etc/ssl/certs/aesc022-va-1-1.serverpod.net.cer',
            'key': '/etc/ssl/private/aesc022-va-1-1.serverpod.net.key'
        },
        'helo_string':  'AESv2 Core Inbound',
        'data_size_limit': 62914560,
    },
    'outbound': {
        'class': 'aes.services.OutboundSMTPService',
        'host': '0.0.0.0',
        'port': 1026,
        'ssl': None,
        'starttls': {
            'cert': '/etc/ssl/certs/aesc022-va-1-1.serverpod.net.cer',
            'key': '/etc/ssl/private/aesc022-va-1-1.serverpod.net.key'
        },
        'helo_string':  'AESv2 Core Outbound',
        'data_size_limit': 62914560,
    },
    'forks': {
        'class': 'aes.services.ForksService',
        'count': multiprocessing.cpu_count(),
    },
    'sender': {'class': 'aes.services.EmailSenderService'},
    'prometheus': {'class': 'aes.services.PrometheusService'},
    'web': {'class': 'aes.services.WebService'},
    'config': {'class': 'aes.services.ConfigService'},
    'analytics': {
        'class': 'aes.services.DirectLogstashService',
        'host': '127.0.0.1',
        'port': 11011,
    },
}

ENGINES = {
    'sophos': {
        'class': 'aes.engines.SophosEngine',
        'host': '127.0.0.1', 
        'port': 4010,
        'timeout': 60,
        'retry_attempts': 3,
        'limit': 10,
        'fast_plain_text': True,
        'ignore_errors': ['020F', '0211', '0212', '021A', '021D', '0225', '0237'],
        'scan_errors': ['0202', '0208', '0209', '0210', '0213', '0215'],
    },
    'cloudmark': {'class': 'aes.engines.CloudmarkEngine'},
    'vade_retro': {
        'class': 'aes.engines.VadeRetroEngine',
        'host': '127.0.0.1',
        'port': 11025,
        'timeout': 60,
        'retry_attempts': 3,
        'limit': 10,
        'cache_ttl': 15*60,
        'cache_lru': 5000,
    },
    'mail_flow': {
        'class': 'aes.engines.MailFlowEngine',
        'internal_hosts': ['10.0.0.0/8'],
        'source_ip_missed': [
            {
                'peer': ['127.0.0.1'],
                'chain': [],
            },
            {
                'peer': ['10.0.0.0/8'],
                'chain': [
                    ['aesmt*.serverpod.net'],
                    ['*.intermedia.net']
                ],
            },
        ],
        'source_ip_present': [
            {
                'peer': ['10.0.0.0/8'],
                'chain': [
                    ['aesmt*.serverpod.net'],
                    [
                     '*.intermedia.net',
                     '*.serverdata.net',
                     '*.serverpod.net',
                     '*.msoutlookonline.net'
                    ]
                ],
            },
        ],
    },
}

FILTERS = [
    ('loop_checker', {
        'class': 'aes.filters.LoopChecker',
        'loop_limit': 5,
        'keep_timeout': 15 * 60,
    }),
    ('mail_flow', {
        'class': 'aes.filters.MailFlowFilter',
        'action': 'bypass'
    }),
    ('external_messages', {'class': 'aes.filters.ExternalMessageCheck'}),
    ('white_black', {'class': 'aes.filters.WhiteBlackFilter'}),
    ('tls_check', {'class': 'aes.filters.TLSCheckFilter'}),
    ('spf', {'class': 'aes.filters.SPFFilter'}),
    ('sophos', {'class': 'aes.filters.SophosFilter'}),
    ('vade_retro_av', {'class': 'aes.filters.VadeRetroAVFilter'}),
    ('spam', {'class': 'aes.filters.SpamFilter'}),
    ('marketing', {'class': 'aes.filters.MarketingFilter'}),
    ('attachments', {'class': 'aes.filters.AttachmentsFilter'}),
    ('phishing', {'class': 'aes.filters.PhishingFilter'}),
    ('url_protection', {
        'class': 'aes.filters.UrlProtectionFilter',
        'urlresolver_url': 'https://url.emailprotection.link',
        'secret_key': 'lORSLyxpMKrLCwadEiNbCiUtTOwipGVC',
        'current_prefix': 'a',
        'action': 'admin_quarantine',
        'links_limit': 1000,
    }),
    ('content', {
        'class': 'aes.filters.ContentFilter',
        'searcher': 'simple',
        'headers': ['From', 'To', 'Subject', 'Reply-To', 'Content-Disposition'],
    }),
]

POLICY_SERVICE = {
    'url': "http://uppls-va-1.wh.intermedia.net:80",
    'pool_limit': 0,
    'timeout': 60,
    'ttl': 5*60,
    'lru': 1000,
    'content_limit': 1024 * 1024 * 3,
    'secret_key': '0123456789ABCDEF0123456789ABCDEF',
}

DELIVERY = {
    'send': {
        'class': 'aes.delivery.ConservativeSendDelivery',
        'command_encoding': 'utf-8',
        'host': 'aesmt022-va-1.serverpod.net',
        'port': 10025,
        'out_host': 'aesomt-va-1.serverpod.net',
        'out_port': 10025,

        'starttls': {
            'cert': '/etc/ssl/certs/aesc022-va-1-1.serverpod.net.cer',
            'key': '/etc/ssl/private/aesc022-va-1-1.serverpod.net.key'
        },
    },
    'admin_quarantine': {
        'class': 'aes.delivery.AdminQuarantineDelivery',
        'command_encoding': 'utf-8',
        'ssl': None,
        'starttls': {
            'cert': '/etc/ssl/certs/aesc022-va-1-1.serverpod.net.cer',
            'key': '/etc/ssl/private/aesc022-va-1-1.serverpod.net.key'
        },
    },
    'user_quarantine': {
        'class': 'aes.delivery.UserQuarantineDelivery',
        'command_encoding': 'utf-8',
        'ssl': None,
        'starttls': {
            'cert': '/etc/ssl/certs/aesc022-va-1-1.serverpod.net.cer',
            'key': '/etc/ssl/private/aesc022-va-1-1.serverpod.net.key'
        },
    },
    'deny': {
        'class': 'aes.delivery.DeliveryService',
    },
    'ndr': {
        'class': 'aes.delivery.ndr.NDRDelivery',
        'starttls': {
            'cert': '/etc/ssl/certs/aesc022-va-1-1.serverpod.net.cer',
            'key': '/etc/ssl/private/aesc022-va-1-1.serverpod.net.key'
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(name)s %(levelname)s %(asctime)s %(message)s %(extra)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s %(extra)s'
        },
    },
    'filters': {
        'user_context': {
            '()': 'aes.core.filters.ContextFilter'
        },
        'console_filter': {
            '()': 'aes.core.filters.ConsoleFilter'
        }
    },
    'handlers': {
        'null': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'ext://os.devnull',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'filters': ['console_filter'],
            'formatter': 'simple',
            'stream': 'ext://sys.stderr',
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'filters': ['console_filter'],
            'formatter': 'simple',
            'address': ('10.216.233.19', 514),
            'facility': 'mail',
        },
        'logstash': {
            'level': 'DEBUG',
            'class': 'aes.services.analytics.logstash.LogstashClusterHandler',
            'filters': ['user_context'],
            'hosts': [('127.0.0.1', 11011)],
            'version': 1,
        },
    },
    'loggers': {
        'aiohttp.access': {
            'level': 'WARNING',
            'propagate': False,
        },
        'elasticsearch': {
            'level': 'ERROR',
        },
        'startup': {
            'level': 'INFO',
            'handlers': ['console'],
        }
    },
    'root': {
        'handlers': ['syslog', 'logstash'],
        'level': 'WARNING',
    }
}