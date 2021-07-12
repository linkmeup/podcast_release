with open("event_template.ics") as f:
    event_template = f.read()

start_time = "20210718T160000"
date, time = start_time.split("T")
time = int(time) + 20000
end_time = f"{date}T{time}"
event = event_template.format(start_time, end_time, "abra-kadabra")

print(event)

with open("telecom.ics", "w") as f:
    f.write(event)
