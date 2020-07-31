#!/usr/bin/env python3


def mutate(method):
  def newmethod(*args, **kwargs):
    """

    The @annotation example @mutate will wrap myfunction with the mutation function.
    Thus, the myfunction will be passed as a parameter to mutate().
    The pratical effect in this example is to sandwich, so to say:
      - a pre-executing code,
      - the myfunction code and, then,
      - a post-executing code.
    The pattern is useful whenever this is a set of pre-tasks and another set of post-tasks,
    As a example, in Flask, or in web frameworks in general,
      one can program both a pre-response and a post-response method wrapping up a view function.

    :param args:
    :param kwargs:
    :return:
    """
    print('Executing method')
    method(*args, **kwargs)  # *args,
    print('Finished Executing method')
  return newmethod


@mutate
def myfunction(a=None, b=None, **kwargs):
  print('hello', a, b, kwargs)


myfunction(1, 2, bla='blah')
