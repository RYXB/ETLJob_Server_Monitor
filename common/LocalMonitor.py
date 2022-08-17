import psutil

#监控本地

def get_ecs_cpu_and_memory():
    data = psutil.virtual_memory()
    total = data.total  # 总内存,单位为byte
    total = round(total / 1024 / 1024 / 1024, 2)  # 转换成GB
    free = data.available  # 可用内存
    free = round(free / 1024 / 1024 / 1024, 2)  # 转换成GB
    disk = "disk usage:%0.2f" % psutil.disk_usage('/').percent + "%" # 硬盘使用情况
    memory = "Memory usage:%0.2f" % (int(round(data.percent))) + "%"  # 内存使用情况
    cpu = "CPU:%0.2f" % psutil.cpu_percent(interval=1) + "%"  # CPU占用情况
    return cpu, memory, total, free ,disk


if __name__ == "__main__":
    cpu, memory, total, free ,disk = get_ecs_cpu_and_memory()
    print('cpu', cpu)
    print('memory', memory)
    print('total: {} GB'.format(total))
    print('free: {} GB'.format(free))
    print('disk', disk)

