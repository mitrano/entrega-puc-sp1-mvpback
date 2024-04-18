from logging.config import dictConfig
import logging
import os

# Define o caminho onde os arquivos de log serão armazenados
log_path = "log/"
# Verifica se o diretório para armazenar os logs não existe
if not os.path.exists(log_path):
    # Caso o diretório não exista, cria o diretório
    os.makedirs(log_path)

# Configuração de logging usando dicionário para definir múltiplos aspectos como formatação e manipuladores
dictConfig({
    "version": 1,  # Indica a versão da configuração do logging
    "disable_existing_loggers": True,  # Desativa os loggers existentes para evitar duplicações
    "formatters": {  # Definições de como as mensagens de log devem ser formatadas
        "default": {  # Formatação padrão para saídas mais simples
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s",
        },
        "detailed": {  # Formatação detalhada inclui o caminho do arquivo para ajudar na depuração
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s - call_trace=%(pathname)s L%(lineno)-4d",
        }
    },
    "handlers": {  # Manipuladores que determinam para onde enviar as mensagens de log
        "console": {  # Saída de log para o console
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "error_file": {  # Arquivo de log para erros, usando um handler que suporta rotação de arquivo
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "log/gunicorn.error.log",
            "maxBytes": 10000,  # Tamanho máximo do arquivo antes de criar um novo arquivo
            "backupCount": 10,  # Número máximo de arquivos de backup a manter
            "delay": "True",  # Atrasa a criação do arquivo até que ele seja necessário pela primeira vez
        },
        "detailed_file": {  # Arquivo de log para informações detalhadas, com configurações semelhantes ao de erros
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "log/gunicorn.detailed.log",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": "True",
        }
    },
    "loggers": {  # Configuração específica para o logger 'gunicorn.error'
        "gunicorn.error": {
            "handlers": ["console", "error_file"],
            "level": "INFO",
            "propagate": False,  # Impede que os logs se propaguem para o logger pai
        }
    },
    "root": {  # Configuração do logger raiz, que captura logs de todos os níveis acima do INFO
        "handlers": ["console", "detailed_file"],
        "level": "INFO",
    }
})

# Cria uma instância do logger para ser usada neste módulo
logger = logging.getLogger(__name__)
