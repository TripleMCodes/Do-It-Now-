Ahh, I see the problem 👀

Your **route** is defined as:

```python
@app.route('/saveTask/<task>', methods=['POST'])
def saveTask(task):
```

That means Flask expects **two things**:

1. The URL must contain a `<task>` part (e.g., `/saveTask/DoHomework`).
2. The HTTP method must be `POST`.

But in your **fetch request**, when you click the button, the request goes to:

```js
fetch(`/saveTask/${task}`, {
    method: 'POST' 
})
```

⚠️ If `task` is empty (like an empty string), the final URL becomes `/saveTask/`, which **does not match** `/saveTask/<task>`. That mismatch gives you the `405 METHOD NOT ALLOWED`.

---

### ✅ Fix Options:

**Option 1: Ensure `task` isn’t empty**

```js
function saveTask() {
    let task = inputTask.value.trim();
    if (!task) {
        console.error("Task is empty, not saving!");
        return;
    }

    fetch(`/saveTask/${task}`, {
        method: 'POST'
    }).then(response => {
        if (response.ok) {
            console.log('The task is saved');
        } else {
            console.log('Failed to save task');
        }
    }).catch(error => {
        console.error("An error occurred while making request: ", error);
    });
}
```

---

**Option 2: Don’t pass task in the URL, send it in the body (cleaner design)**

```python
@app.route('/saveTask', methods=['POST'])
def saveTask():
    data = request.get_json()
    task = data.get("task")
    date = datetime.now()
    print(f'the task: {task} the date {date}')
    return ""
```

```js
function saveTask() {
    let task = inputTask.value.trim();
    if (!task) {
        console.error("Task is empty, not saving!");
        return;
    }

    fetch(`/saveTask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
    }).then(response => {
        if (response.ok) {
            console.log('The task is saved');
        } else {
            console.log('Failed to save task');
        }
    }).catch(error => {
        console.error("An error occurred while making request: ", error);
    });
}
```

---

👉 Personally, I’d recommend **Option 2** (using JSON in the body). It scales better if later you want to send extra info (like `due_date`, `priority`, etc.).

Do you want me to refactor your code fully into the Option 2 (clean JSON approach), or do you prefer to stick with the URL approach for now?
---
---
---
Got it 👍 your delete route looks *almost* right, but there are a couple of things that can trip it up. Let’s troubleshoot systematically:

---

### ✅ Checklist of Common Issues

1. **Is the request actually sending JSON?**
   Your route is doing:

   ```python
   data = request.get_json()
   task = data.get("task")
   ```

   If the fetch request didn’t include a `Content-Type: application/json` header, `request.get_json()` will return `None`.
   Then `data.get("task")` throws an error or `task` is `None`, so nothing is deleted.

   👉 In JS you need:

   ```js
   fetch('/delTask', {
       method: 'DELETE',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ task })
   })
   ```

---

2. **Does the record actually exist?**
   If you run:

   ```python
   deleted = Tasks.query.filter(Tasks.task_name == task).delete()
   logging.debug(f"Deleted count: {deleted}")
   ```

   If `deleted` is `0`, it means no row matched. Possible reasons:

   * Task name mismatch (trailing spaces, case sensitivity, etc.).
   * Maybe you stored `"Do homework"` but you’re sending `"do homework"`.
   * Maybe the column isn’t exactly `task_name`.

---

3. **Flask’s `.delete()` behavior**
   `Query.delete()` bypasses some ORM features (like cascade rules and session flush). Sometimes it’s safer to query the object and delete it:

   ```python
   task_to_delete = Tasks.query.filter_by(task_name=task).first()
   if task_to_delete:
       db.session.delete(task_to_delete)
       db.session.commit()
       logging.debug(f"Deleted task: {task}")
   else:
       logging.debug(f"No task found with name: {task}")
   ```

---

### 🔧 Recommended Fix

```python
@app.route('/delTask', methods=['DELETE'])
def delTask():
    data = request.get_json()
    task = data.get("task")

    logging.debug(f'The task to be deleted is "{task}"')

    task_to_delete = Tasks.query.filter_by(task_name=task).first()
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        logging.debug('Task deleted')
        return '', 200
    else:
        logging.debug('Task not found')
        return '', 404
```

JS fetch:

```js
function deleteTask(task) {
    fetch('/delTask', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task })
    }).then(response => {
        if (response.ok) {
            console.log('Task deleted');
        } else {
            console.log('Task not found');
        }
    }).catch(error => {
        console.error("Error deleting task:", error);
    });
}
```

---

⚡ Question for you: in your DB, are `task_name`s **unique** or can you have multiple tasks with the same name? Because if they’re not unique, `filter_by(task_name=task).first()` will only delete one — but `delete()` would nuke them all. Do you want **single deletion** or **bulk deletion**?
