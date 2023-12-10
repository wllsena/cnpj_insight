from django.core.management import call_command


def backup():
    """Backup the database."""
    try:
        call_command('dbbackup')
    except Exception as e:
        print(e)
