import os
import time
import json

def get_all_raw_os_data():
    raw_data = {}

    raw_data['os_name'] = os.name
    if hasattr(os, 'uname'):
        uname = os.uname()
        raw_data['os_uname'] = {
            "sysname": uname.sysname,
            "nodename": uname.nodename,
            "release": uname.release,
            "version": uname.version,
            "machine": uname.machine
        }
    
    raw_data['os_environ'] = {str(k): str(v) for k, v in os.environ.items()}
    raw_data['pid'] = os.getpid()
    raw_data['ppid'] = os.getppid()
    raw_data['cwd'] = os.getcwd()

    if os.name == 'posix':
        raw_data['uid'] = os.getuid()
        raw_data['gid'] = os.getgid()
        raw_data['groups'] = os.getgroups()
        try:
            raw_data['login'] = os.getlogin()
        except OSError:
            raw_data['login'] = None

    if hasattr(os, 'times'):
        t = os.times()
        raw_data['process_times'] = {
            "user": t.user, "system": t.system, 
            "children_user": t.children_user, "children_system": t.children_system, 
            "elapsed": t.elapsed
        }
        
    if hasattr(os, 'getrusage'):
        import resource
        rusage = os.getrusage(resource.RUSAGE_SELF)
        raw_data['rusage_self'] = [getattr(rusage, attr) for attr in dir(rusage) if attr.startswith('ru_')]

    if hasattr(os, 'getloadavg'):
        raw_data['load_avg'] = os.getloadavg()

    raw_data['time_timestamp'] = time.time()
    raw_data['time_perf_counter'] = time.perf_counter()
    raw_data['time_monotonic'] = time.monotonic()
    raw_data['time_timezone_raw'] = time.timezone
    raw_data['time_tzname'] = list(time.tzname)
    
    for key, struct_t in [('time_struct_local', time.localtime()), ('time_struct_gm', time.gmtime())]:
        raw_data[key] = {
            "tm_year": struct_t.tm_year, "tm_mon": struct_t.tm_mon, "tm_mday": struct_t.tm_mday,
            "tm_hour": struct_t.tm_hour, "tm_min": struct_t.tm_min, "tm_sec": struct_t.tm_sec,
            "tm_wday": struct_t.tm_wday, "tm_yday": struct_t.tm_yday, "tm_isdst": struct_t.tm_isdst
        }

    if hasattr(os, 'sysconf_names'):
        sysconf_data = {}
        for name, code in os.sysconf_names.items():
            if isinstance(code, int) and code >= 0:
                try:
                    sysconf_data[name] = os.sysconf(name)
                except ValueError:
                    continue
        raw_data['sysconf'] = sysconf_data

    return raw_data

def custom_json_serializer(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='ignore')
    return str(obj) 

def save_raw_os_data(file_name="os_raw_data.json"):
    data = get_all_raw_os_data()
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=custom_json_serializer)
    print(f"**Данные успешно сохранены в файл: {os.path.abspath(file_name)}**")
