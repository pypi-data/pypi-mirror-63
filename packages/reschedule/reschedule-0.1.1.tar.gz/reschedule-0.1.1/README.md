# TODO MD Scheduler

## Goal

I want to keep track of all my todos in a [plain text file](https://jeffhuang.com/productivity_text_file/) but also automatically schedule my todos on my google calendar. When I write my todos in a todo list I often fail to allocate time for them in my calendar. When I look at my week I feel like I have tons of free time but in reality I have a full day of work to do. As an example this is what my week looks like without todos vs. with todos (in orange).

![Example week with todos and without todos](img/calendar.gif)

This program automatically parses todos from a markdown file and schedules them on a google calendar.

```markdown
- [ ] task name est:10m due:2020-03-20 id:1f2a4b
```

## Installation

Using python >3.6

`pip install reschedule`

Now you can reschedule your todos by running `reschedule` from the command line.
The first time you run `reschedule` you'll be prompted to authorize with google and a config file will be created for you at `~/.cache/reschedule/config.json`.

## Configuration

```json
{
  "work_start_time": "08:00",
  "work_end_time": "18:00",
  "task_file_path": "~/todo.md",
  "task_calendar_name": "Reschedule Tasks",
  "chunk_size": 15,
  "default_est": "30m"
}
```

- `work_start_time`: the earliest a task will be scheduled to start in `%H:%M` format. (i.e. military time such as 08:30 or 23:00)
- `work_end_time`: the latest a task will be scheduled to end in `%H:%M` format. (i.e. military time such as 08:30 or 23:00)
- `task_file_path`: the absolute path to your markdown file of tasks
- `task_calendar_name`: the name of the google calendar this program will create to store your tasks. **Must be unique from an existing calendar**.
- `chunk_size`: the minimum length of an event. 15 is a good default to keep your day from becoming too fragmented.
- `default_est`: the default time estimate for a task

## Task File Format

Task are written using markdown task-list format. To create a task use a new line with `- [ ]`. To mark a task as complete use `- [x]`. Metadata is attached to tasks using a `key:value` syntax. The `key` and the `value` cannot contain spaces or `:`. I call an instance of a `key:value` pair a tag, for instance an `id` tag is a `key:value` pair with a `key` of `id`. Every task needs a unique `id` tag for example `id:1aab7d`. Tasks can have an `est` tag which contains a time estimate written as `30m` or `1h` for 30 minutes or 1 hour respectively. Any number followed by `m` or `h` is acceptable as a value for the `est` tag. Finally tasks can have a `due` tag which contains a due-date formatted as `YYYY-MM-dd`.

```markdown
<!-- A task with an estimate of 30 minutes, due March 6, 2020, with id 16cfe6 -->

- [ ] What you want to do est:30m due:2020-03-06 id:16cfe6
```

## VSCode Snippets

I use the following user defined [VSCode Markdown Snippets](https://code.visualstudio.com/docs/languages/markdown#_snippets-for-markdown) to create my tasks.

```jsonc
  // add a new task
  "task": {
    "prefix": "//task",
    "body": [
      "- [ ] ${1:What do you want to do?} est:${2:30m} id:$RANDOM_HEX"
    ]
  },
  // add a due date to a task
  "due": {
    "prefix": "//due",
    "body": "due:${1:$CURRENT_YEAR}-${2:$CURRENT_MONTH}-${3:$CURRENT_DATE}"
  },
  // create a random variable
  "random": {
    "prefix": "//random",
    "body": "$RANDOM_HEX"
  }
```
