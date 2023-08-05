# TODO MD Scheduler

## Goal

I have a markdown file of todos which I want to automatically schedule on my google calendar.

```markdown
- [ ] task name @related_person +task_project est:10m id:1f2a4b
```

Each task is assumed to have the following properties

- **id**: a unique id
- **description**: a description of the task
- **estimate**: a time estimate written as `5m` or `2h` for 5 minutes and 2 hours respectively.

This program divides a day into chunks of size 15 minutes and schedules tasks during those chunks. The tasks are added to a unique calendar in Google Calendar.

## Design

`task_parser.py` parses the todo file and creates a list of tagged `task` objects.

`calendar_api.py` is in charge of getting calendar information.
