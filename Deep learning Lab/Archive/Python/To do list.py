class TaskManager:
    
    
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name):
        if task_name.strip():  # Check if task name is not empty
            self.tasks.append([task_name, "incomplete"])
            print(f"Task '{task_name}' added!")
        else:
            print("Task name cannot be empty!")

    def status(self):
        if not self.tasks:
            print("No tasks yet")
            return
        print("Your Task Report")
        completed = []
        ongoing = []
        for index, task in enumerate(self.tasks, 1):  # Fixed: self.task -> self.tasks
            if task[1] == "complete":
                completed.append(f"{index}. {task[0]} - Done, good job!")
            else:
                ongoing.append(f"{index}. {task[0]} - You can do it, keep it up!")  # Fixed: task -> task[0]
        print("Completed Tasks:")
        for line in completed:
            print(line)
        if ongoing:
            print("Ongoing Tasks:")
            for line in ongoing:
                print(line)

    def complete_task(self, task_number):
        if not self.tasks:
            print("No tasks to complete")
            return  # Added return to exit early
        try:
            index = int(task_number) - 1  # Convert to int here
            if 0 <= index < len(self.tasks):
                if self.tasks[index][1] == "complete":
                    print(f"Task '{self.tasks[index][0]}' is already completed!")
                else:
                    self.tasks[index][1] = "complete"
                    print(f"Task '{self.tasks[index][0]}' marked as complete!")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

    def remove_task(self, task_number):
        if not self.tasks:  # Fixed: self.task -> self.tasks
            print("No tasks yet")
            return
        try:
            index = int(task_number) - 1  # Convert to int here
            if 0 <= index < len(self.tasks):
                removed_task = self.tasks.pop(index)
                print(f"Task '{removed_task[0]}' removed!")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

task_manager = TaskManager()

print("Welcome to Your To-Do List Manager!")
print("Enter:")
print("  'add'     - Add a new task")
print("  'remove'  - Remove a task")
print("  'complete' - Mark a task as done")
print("  'report'  - See your daily report")
print("  'exit'    - Finish the procedure")

while True:
    command = input("> ").lower().strip()  # Added strip() for better input handling

    if command == 'add':
        task_name = input("Enter your task: ").strip()
        task_manager.add_task(task_name)
    elif command == "remove":
        if not task_manager.tasks:
            print("No tasks to remove!")
        else:
            print("Your tasks:")
            for index, task in enumerate(task_manager.tasks, 1):
                print(f"{index}. {task[0]} - {task[1]}")
            choice = input("Enter task number to remove (0 to cancel): ").strip()
            if choice == "0":
                print("Removal cancelled")
            else:
                task_manager.remove_task(choice)  # Pass choice directly, conversion handled in method
    elif command == "complete":
        if not task_manager.tasks:
            print("No tasks to complete!")
        else:
            print("Your tasks:")
            for index, task in enumerate(task_manager.tasks, 1):
                print(f"{index}. {task[0]} - {task[1]}")
            choice = input("Enter task number to mark complete (0 to cancel): ").strip()
            if choice == "0":  # Fixed: choice is string, compare with "0"
                print("Completion cancelled.")
            else:
                task_manager.complete_task(choice)  # Pass choice directly, conversion handled in method
    elif command == "report":
        task_manager.status()
    elif command == "exit":
        print("Goodbye!")
        break
    else:
        print("Invalid option! Enter:")
        print("  'add'     - Add a new task")
        print("  'remove'  - Remove a task")
        print("  'complete' - Mark a task as done")
        print("  'report'  - See your daily report")
        print("  'exit'    - Finish the procedure")
