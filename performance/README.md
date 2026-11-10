# Performance Testing (JMeter)

Plan: `restful-booker-load-test.jmx`. Each virtual user repeats three requests:

1. `GET /booking` (list ids)
2. `POST /booking` (create; the booking id is extracted from the response)
3. `GET /booking/{id}` (fetch the booking just created)

Each request asserts HTTP 200, and a 500 ms think time sits between requests.

## Run (non-GUI mode)
Install Apache JMeter 5.6+ and Java 8+, then from the repository root:

```bash
jmeter -n -t performance/restful-booker-load-test.jmx \
  -Jusers=50 -Jrampup=30 -Jloops=5 \
  -l performance/results/results.jtl \
  -e -o performance/results/report
```

On Windows use `jmeter.bat`. The folder `performance/results/report` must not exist before the run. Open `performance/results/report/index.html` for the dashboard.

| Property | Default | Meaning |
|---|---|---|
| `users` | 50 | Concurrent virtual users |
| `rampup` | 30 | Seconds to start all users |
| `loops` | 5 | Iterations per user |

Scenarios: TC-032 (`users=50 rampup=30`) and TC-033 (`users=100 rampup=60`).

## Be considerate
The target is a shared public demo API. Do not go above 100 users, and keep each run short.

## Report
After each run, copy the numbers from the dashboard into `performance-report-template.md`. Do not publish numbers you did not measure.
