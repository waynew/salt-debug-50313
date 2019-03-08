import csv
import datetime
import json
import re
import subprocess
import time

from collections import defaultdict


TEMPLATE = '''<!DOCTYPE html>
<body>
<canvas id="chart" width="600" height="600"></canvas>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>
<script>
var ctx = document.getElementById("chart").getContext('2d');
ctx.canvas.width = 600;
ctx.canvas.width = 600;
var chart = new Chart(ctx, {{
  type: 'line',
  data: {{
      labels: {labels},
      datasets: {datasets},
  }},
  options: {{
    scales: {{
      xAxes: [{{
        type: 'time',
        distribution: 'series',
      }}],
    }},
  }},
}});
</script>
</body>
</html>
'''


def hexlify(name):
    num = int(re.sub('[^a-zA-Z0-9]', '', name), 36)
    return '#'+hex(num)[2:8].zfill(6)


def render_html(data):
    labels = set()
    for name in data:
        for ts, _ in data[name]:
            labels.add(ts)
    labels = list(sorted(labels))
    datasets = []
    for name in data:
        datasets.append({
            'data': [d[1] for d in data[name]],
            'label': name,
            'borderColor': hexlify(name),
            'fill': False,
        })

    render = TEMPLATE.format(labels=json.dumps(labels), datasets=json.dumps(datasets))
    with open('index.html', 'w') as f:
        f.write(render)


def parsemem(vals):
    vals = vals.strip()
    if vals.endswith('MiB'):
        factor = 1
        amount = float(vals[:-3])
    elif vals.endswith('GiB'):
        factor = 1000
        amount = float(vals[:-3])*factor
    else:
        print('Unknown', vals[-4:])
        amount = 0
    return amount


def do_it():  # Shia LeBeouf
    data = defaultdict(list)
    try:
        with open('data.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                name, timestamp, mbytes = row
                data[name].append((timestamp, mbytes))
    except FileNotFoundError:
        pass  # It's fine if there's no data yet

    while True:
        results = subprocess.run(
            [
                'docker',
                'stats',
                '--all',
                '--format',
                'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}',
                '--no-stream',
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        output = results.stdout.decode()
        timestamp = datetime.datetime.now()
        for line in output.split('\n')[1:]:
            if not line.strip(): continue
            name, cpu, memdata = line.split(None, maxsplit=2)
            used, _, avail = memdata.partition('/')
            used = parsemem(used)
            avail = parsemem(avail)
            with open('data.csv', 'a+') as f:
                writer = csv.writer(f)
                writer.writerow((name, timestamp, used))
                data[name].append((str(timestamp), used))

        render_html(data)
        time.sleep(1)


if __name__ == '__main__':
    try:
        do_it()
    except KeyboardInterrupt:
        print('^C caught, goodbye!')
