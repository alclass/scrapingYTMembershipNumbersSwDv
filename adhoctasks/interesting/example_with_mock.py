#!/usr/bin/env python3
"""
  docstring
"""


def get_user_input():
  """
  if robot.lower() == 'n':
    return f"You are {first_name} {last_name} and you're {age} years old"
  if robot.lower() == 'y':
    return f"Welcome, my artificial friend"
  return f"You are not a human or a bot, then what are you?"

  :return:
  """
  first_name = input('Enter your first name: ')
  last_name = input('Enter your last name: ')
  age = int(input('Enter your age: '))
  robot = input('Are you a robot? (y/n) ')
  return f"You are {first_name} {last_name} and you're {age} years old"


def process():
  retstr = get_user_input()
  print(retstr)


if __name__ == '__main__':
  process()
