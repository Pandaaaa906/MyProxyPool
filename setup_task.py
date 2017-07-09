import inspect
import math
import peewee
import models
from models import IPTask

l_models = [
    obj for name, obj in inspect.getmembers(
        models, lambda obj: inspect.isclass(obj) and issubclass(obj, peewee.Model)
    )
]

peewee.create_model_tables(l_models, fail_silently=True)
with open("delegated-apnic-latest.txt", 'r') as f:
    for line in f:
        if line.startswith("#"):
            continue
        row = line.strip().split("|")
        if len(row) == 7:
            _, country, ip_type, start_ip, n, date, state = row
            if country == "CN" and ip_type == "ipv4":
                t_range = int(32-math.log(int(n),2))
                if IPTask.select().where(IPTask.start_ip==start_ip).exists():
                    IPTask.update(t_range=t_range).where(IPTask.start_ip==start_ip)
                else:
                    IPTask.create(start_ip=start_ip,
                                  t_range=t_range
                                  )
