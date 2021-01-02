import os
import json
import argparse

TODO_FILENAME = '.todo'


def write_todo_file(data: list):
	"""our to-do data is a list of dict objects,
	with task:str, checked:bool and id:int keys"""
	with open(TODO_FILENAME, 'w') as file:
		json.dump(data, file, indent=2)


def read_todo_file() -> list:
	""""we'll use this function to read our to-do file.
	this funtion will try to read a file named '.todo',
	and create it if doesnt exist.
	"""
	# check if the file exists
	if os.path.exists(TODO_FILENAME):
		# if it exists, the load the data and return it
		with open(TODO_FILENAME) as file:
			result: list = json.load(file)
		return result
	# else just write sand return an empty list
	write_todo_file([])
	return []


def generate_todo_id(todo_list: list) -> int:
	""" get the to-do with the biggest id in the to-do list,
	and return a number bigger than it by one. """
	if not todo_list:
		# just return 0 if there no items in the list
		return 0
	max_id_todo: dict = max(todo_list, key=lambda todo: todo.get("id", 0))
	max_id: int = max_id_todo.get("id", 0)
	return max_id + 1


def add_todo(task: str):
	"""this function will get the to-do list,
	add a to-do to the list,
	then save the list."""
	todo_list: list = read_todo_file()
	todo = dict(
		id=generate_todo_id(todo_list),
		task=task,
		checked=False
	)
	todo_list.append(todo)
	write_todo_file(todo_list)


# noinspection PyShadowingBuiltins
def delete_todo(id: int):
	"""iterates through the to-do list,
	and filters the to-do... removing the one who's id matches $id"""
	todo_list: list = read_todo_file()
	todo_list = [todo for todo in todo_list if not (todo.get("id") == id)]
	write_todo_file(todo_list)


# noinspection PyShadowingBuiltins
def check_todo(id: int, state: bool):
	"""iterates through the to-do list,
	and sets the to-do item with the matching id, checked to $state"""
	todo_list: list = read_todo_file()
	for todo in todo_list:
		if todo.get("id") == id:
			todo["checked"] = state
			break
	write_todo_file(todo_list)


def print_todo_list():
	todo_list: list = read_todo_file()
	for todo in todo_list:
		todo["checked"] = "checked" if todo.get("checked", False) else "not checked"
		print("{id} [{checked}] {task}".format(**todo))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog="todo",
		description="a simple cli app for managing todo",
		allow_abbrev=False
	)

	# arg for passing id
	parser.add_argument(
		"-i", "--id",
		action="store",
		type=int,
		help="specify a todo-items id"
	)

	# args for creating a new to-do item
	parser.add_argument(
		"-t", "--task",
		action="store",
		type=str,
		help="create a new todo item"
	)

	# args for deleting a to-do item
	parser.add_argument(
		"-d", "--delete",
		action="store_true",
		help="deletes a todo item with the given id"
	)

	# args to check a to-do item
	parser.add_argument(
		"-c", "--check",
		action="store",
		type=int,
		help="checkes or uncheckes a todo item [0|1]"
	)

	# arg print the to-do lisy
	parser.add_argument(
		"--print",
		action="store_true",
		help="prints the todo list"
	)

	args = parser.parse_args()

	# editing operation
	if not (args.id is None):

		if args.delete:
			# ... delete to-do
			delete_todo(args.id)

		if args.check:
			# ... check to-do
			check_todo(args.id, bool(args.check))

	# add operation
	else:

		if args.task:
			add_todo(args.task)

	# ...
	if args.print:
		print_todo_list()
