//Variables

const addTask = document.getElementById('add-task');
const taskContainer = document.getElementById('task-container');
const inputTask = document.getElementById('input-task')
let chckBtn = document.querySelectorAll('.checkTask')
let delBtn = document.querySelectorAll('.deleteTask')
let taskHolder = '' //holds input value to pass to saveTask



//events to button
function saveTask() {
   
    task = taskHolder;
    if (!task) {
        console.info("The is empty");
        return;
    }
    fetch(`/saveTask`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({task})
    }).then(response => {
        if (response.ok) {
            console.log('The task is saved');
        }
        else {
            console.log('Failed to save task');
        }
    }).catch(error => {
        console.error("An occured while making request: ", error);
    })
}

function deleteTask() {
    task = String(this.previousElementSibling.previousElementSibling.innerText.trim());
    console.log('The task is: ', task);

    fetch(`/delTask`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({task})
    }).then(response => {
        if (response.ok) {
            console.info('Task deleted');
        }
        else {
            console.warn("Couldn't save task");
        }
    }).catch(error => {
        console.error('An error occured while deleting app ', error);
    })
}
//Event listener for add button

addTask.addEventListener('click', function () {
    
    let task = document.createElement('div');
    task.classList.add('task');

    taskHolder = inputTask.value.trim();

    let li = document.createElement('li')
    li.innerText = `${inputTask.value}`;
    task.appendChild(li);

    let checkButton = document.createElement('button');
    checkButton.innerHTML = '<i class="fa-solid fa-check"></i>';
    checkButton.classList.add('checkTask');
    task.appendChild(checkButton);

    let deleteButton = document.createElement('button');
    deleteButton.innerHTML = '<i class="fa-solid fa-trash-can"></i>';
    deleteButton.classList.add('deleteTask');
    task.appendChild(deleteButton);

    if (inputTask.value === "") {
        alert('Please enter a task');
    }
    else {
        taskContainer.appendChild(task);
        console.log(task);
        console.log("Item appended");
    }
    inputTask.value = "";

    checkButton.addEventListener('click', function () {
        checkButton.parentElement.style.textDecoration = 'line-through';
        checkButton.classList.add("done")
    })
    checkButton.addEventListener('click', markDone);
    checkButton.addEventListener('click', () => {
        if (checkButton.classList.contains("done")) {
            checkButton.disabled = true;
        }
    });

    deleteButton.addEventListener('click', function () {
        task.remove();
    })
    deleteButton.addEventListener('click', deleteTask);
});

addTask.addEventListener('click', saveTask)

chckBtn.forEach(element => {
    element.addEventListener('click', () => {
        element.parentElement.style.textDecoration = 'line-through';
        disableEle(element);
    }) 
});
delBtn.forEach(element => {
    element.addEventListener('click', deleteTask);
    element.addEventListener('click', () => {
        element.parentElement.remove();
    });
    
});

function markDone() {
    task = this.previousElementSibling.innerText;
    if (task) {
        fetch("/taskdone", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({task})
        }).then(response => {
            if (response.ok) {
                console.info('Task marked as done');
            }
            else {
                console.warn("Couldn't save task");
            }
        }).catch(error => {
            console.error(`An occured ${error}`);
        })
    }
    
};
function disableEle(ele) {
    ele.disabled = true;
}

chckBtn.forEach(element => {
    liEle = element.previousElementSibling;
    console.log(liEle)
    console.info(`the class list is ${liEle.classList}`)
    if (liEle.classList == "done") {
        disableEle(liEle);
    }
    else {
        element.addEventListener('click', markDone)
    }
});



