import re
import datetime
import subprocess
from honeypot_utils import get_logger

# logger
logger = get_logger(__name__)

def supervisor(journal, regex, last_check):
    """
    Analyse the file to find regex
    
    search for the specific regex in the file
    Arguments:
        journal: log file to analyse
        regex: regular expression to apply
        last_check: previous analyse datetime
    returns:
        tuple of blocked hosts
    """
    with open(journal) as hp:
        logs = hp.read()
    
    logger.debug(regex)
    pattern = re.compile(regex)
    lines = pattern.finditer(logs)
    #list of hosts blocked
    hosts_blocked = []
    if lines:
        for line in lines:
            year = _get_value(line,'year')
            month = _get_value(line,'month')
            day = int(_get_value(line,'day'))
            hour = int(_get_value(line,'hour'))
            minute = int(_get_value(line,'minute'))
            host = _get_value(line,'host')
            logger.debug('%s found in inspected file' %host)
            month = _month_to_int(month)
            handled = _is_line_handled(last_check, year, 
                month, day, hour, minute)
            if not handled:
                _ban_host(host)
                hosts_blocked.append(host)
    
    return tuple(hosts_blocked)
    
def _get_value(result, key):
    """
    Helper to get values from the regex result

    Arguments:
        result: a regex result
        key: key 
    
    return:
        value
    """
    try:
        value = result.group(key)
    except IndexError as e:
        value = None
    return value

def _is_line_handled(last_check, year, month, day, hour, minute):
    """
    Check if log has been handled according to the date
    """
    #current date
    now  = datetime.datetime.now()
    # if year is not in the log line, add current yean
    if year is None:
        year = now.year
        
    log_date = datetime.datetime(year, month, day, hour, minute)
    # log_date can not be great than current date
    # so, year has to be decreased
    if log_date > now:
        log_date = log_date.replace(year=log_date.year-1)

    logger.debug('last_check %s, log_date %s' %(last_check, log_date))
    # difference between last check and log date
    delta = log_date - last_check 
    return log_date > last_check
    
def _ban_host(host):
    """
    add an iptables rule to ban a host
    """
    command  = "touch /tmp/OO1.test"
    returncode = subprocess.call(command.split())
    logger.info("'%s' executed, exit code %s" %(command, returncode))

def _unban_host(host):
    """
    remove an iptables rule to unban a host
    """
    #TODO add command
    command  = ""
    #TODO log execution code
    returncode = subprocess.call(command.split())
    print("returncode for %s" %command)
    #Todo log return code
    
def _month_to_int(month):
    """
    convert month to integer
    """
    if type(month) is int:
        return month
    
    corr = {'jan':1,
        'feb':2,
        'mar':3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12}
    month = month.lower()
    return corr[month]
    
