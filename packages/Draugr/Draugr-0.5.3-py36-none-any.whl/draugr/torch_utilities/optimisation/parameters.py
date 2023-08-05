#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/02/2020
           """

__all__ = ["frozen_parameters", "freeze_parameters", "freeze_model", "frozen_model"]

from typing import Iterator


from torch.nn import Module, Parameter
from contextlib import contextmanager
from itertools import tee


def freeze_model(model: Module, value: bool = None, recurse: bool = True) -> None:
    """

  :param recurse:
  :param params:
  :param value:
  :return:
  """
    freeze_parameters(model.parameters(recurse), value)


def freeze_parameters(params: Iterator[Parameter], value: bool = None) -> None:
    """

  :param params:
  :param value:
  :return:
  """
    if isinstance(value, bool):
        for p in params:
            p.requires_grad = not value
    else:
        for p in params:
            p.requires_grad = not p.requires_grad


@contextmanager
def frozen_model(model: Module, recurse: bool = True, enabled=True) -> None:
    """

  :param model:
  :param recurse:
  :return:
  """
    params_1, params_2 = tee(model.parameters(recurse))
    if enabled:
        freeze_parameters(params_1, True)
    yield True
    if enabled:
        freeze_parameters(params_2, False)


@contextmanager
def frozen_parameters(params: Iterator[Parameter], enabled=True) -> None:
    """

  :param params:
  :return:
  """
    params_1, params_2 = tee(params)
    if enabled:
        freeze_parameters(params_1, True)
    yield True
    if enabled:
        freeze_parameters(params_2, False)


if __name__ == "__main__":
    from torch import nn

    def asda():
        a = nn.Linear(10, 5)
        print(a.weight.requires_grad)
        with frozen_model(a):
            print(a.weight.requires_grad)
        print(a.weight.requires_grad)

    def asd21312a():
        a = nn.Linear(10, 5)
        print(a.weight.requires_grad)
        with frozen_parameters(a.parameters()):
            print(a.weight.requires_grad)
        print(a.weight.requires_grad)

    def afsda32():
        a = nn.Linear(10, 5)

        print(a.weight.requires_grad)
        with frozen_parameters(a.parameters()):
            print(a.weight.requires_grad)
        print(a.weight.requires_grad)

    def afsda12332_toogle():
        a = nn.Linear(10, 5)

        print(a.weight.requires_grad)
        freeze_parameters(a.parameters())
        print(a.weight.requires_grad)
        freeze_parameters(a.parameters())
        print(a.weight.requires_grad)

    def afsda12332_explicit():
        a = nn.Linear(10, 5)

        print(a.weight.requires_grad)
        freeze_parameters(a.parameters(), True)
        print(a.weight.requires_grad)
        freeze_parameters(a.parameters(), False)
        print(a.weight.requires_grad)

    def seq_no_context():
        a = nn.Sequential(nn.Linear(10, 5), nn.Linear(5, 5))

        print(next(a.parameters()).requires_grad)
        freeze_parameters(a.parameters(), True)
        print(next(a.parameters()).requires_grad)
        freeze_parameters(a.parameters(), False)
        print(next(a.parameters()).requires_grad)

    def seq_context():
        a = nn.Sequential(nn.Linear(10, 5), nn.Linear(5, 5))

        print(next(a.parameters()).requires_grad)
        freeze_parameters(a.parameters(), True)
        print(next(a.parameters()).requires_grad)
        freeze_parameters(a.parameters(), False)
        print(next(a.parameters()).requires_grad)

    asda()
    print("\n")
    asd21312a()
    print("\n")
    afsda32()
    print("\n")
    afsda12332_toogle()
    print("\n")
    afsda12332_explicit()
    print("\n")
    seq_no_context()
    print("\n")
    seq_context()
