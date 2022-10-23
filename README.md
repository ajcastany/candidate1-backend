# CandidateApp backend

This is a Flask webserver with SQLAlchemy library for interacting with the postgres database.  It serves the API for the CandidateApp frontend.

## PostgreSQL

This api connects to a PostgreSQL db with two tables: **staff** and **daily_form**:

### `staff` table columns:

| Column     | Data type                        |
|------------|----------------------------------|
| id         | Primary Key, auto-increment, int |
| name       | varchar(50)                      |
| department | varchar(50)                      |

### `daily_form` table columns:

| Column   | Data type                        |
|----------|----------------------------------|
| id       | Primary Key, auto-increment, int |
| day      | date                             |
| name     | Foreign key, ref staff(id), int  |
| room     | varchar(10)                      |
| time_in  | time                             |
| time)out | time                             |
| tag      | varchar(10)                      |
| tag_ret  | boolean                          |

## API endpoints:

#### GET
- `/api/staff/all` returns an Ascending list of all staff names in the database.
- `/api/staff{id}` returns `{name, department}` function deprecated
- `/api/dailyform/day/{day}` returns `{id, name, room, time_in, time_out, tag, tag_ret, staff.name, staff.department}` for each entry for the day in `{day}`
- `/api/daily_form/row_id/{row_id}` **TESTING ONLY** returns `{id, name, room, time_in, time_out, tag, tag_ret, staff.name, staff.department}` for the row id.
- `/api/daily_form/all_days` **TESTING ONLY** returns all entries of the daily_form database

#### POST

- `/api/daily_form/room` posts string meeting room on row id from json request.
- `/api/daily_form/time` posts dtype:time time in or time out on row id from json request.
- `/api/daily_form/tag`  posts string tag number on row id from json request.
- `/api/daily_form/tag_ret` posts boolean tag_ret on row id from json request.

#### PUT
- `/api/daily_form/add_new_entry` creates a new entry from json request on database

#### DELETE
- `/api/daily_form/delete_entry/{entry_to_delete}` deletes row where id == `{entry_to_delete}`.



