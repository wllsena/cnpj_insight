from django.core.management import call_command
def backup():
    try:
        call_command('dbbackup')
    except Exception as e:
        print(e)