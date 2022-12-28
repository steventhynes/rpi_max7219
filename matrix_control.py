import RPi.GPIO as gpio
import time
import requests
import queue
import datetime

chars = [
    3, 8, [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # space
    1, 8, [0,1,0,1,1,1,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # !
    3, 8, [0,0,0,0,0,0,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # "
    5, 8, [0,0,0,1,0,1,0,0], [0,0,1,1,1,1,1,0], [0,0,0,1,0,1,0,0], [0,0,1,1,1,1,1,0], [0,0,0,1,0,1,0,0], # #
    4, 8, [0,0,1,0,0,1,0,0], [0,1,1,0,1,0,1,0], [0,0,1,0,1,0,1,1], [0,0,0,1,0,0,1,0], [0,0,0,0,0,0,0,0], # $
    5, 8, [0,1,1,0,0,0,1,1], [0,0,0,1,0,0,1,1], [0,0,0,0,1,0,0,0], [0,1,1,0,0,1,0,0], [0,1,1,0,0,0,1,1], # %
    5, 8, [0,0,1,1,0,1,1,0], [0,1,0,0,1,0,0,1], [0,1,0,1,0,1,1,0], [0,0,1,0,0,0,0,0], [0,1,0,1,0,0,0,0], # &
    1, 8, [0,0,0,0,0,0,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # '
    3, 8, [0,0,0,1,1,1,0,0], [0,0,1,0,0,0,1,0], [0,1,0,0,0,0,0,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # (
    3, 8, [0,1,0,0,0,0,0,1], [0,0,1,0,0,0,1,0], [0,0,0,1,1,1,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # )
    5, 8, [0,0,1,0,1,0,0,0], [0,0,0,1,1,0,0,0], [0,0,0,0,1,1,1,0], [0,0,0,1,1,0,0,0], [0,0,1,0,1,0,0,0], # *
    5, 8, [0,0,0,0,1,0,0,0], [0,0,0,0,1,0,0,0], [0,0,1,1,1,1,1,0], [0,0,0,0,1,0,0,0], [0,0,0,0,1,0,0,0], # +
    2, 8, [1,0,1,1,0,0,0,0], [0,1,1,1,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # ,
    4, 8, [0,0,0,0,1,0,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,0,0,0,0], # -
    2, 8, [0,1,1,0,0,0,0,0], [0,1,1,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # .
    4, 8, [0,1,1,0,0,0,0,0], [0,0,0,1,1,0,0,0], [0,0,0,0,0,1,1,0], [0,0,0,0,0,0,0,1], [0,0,0,0,0,0,0,0], # /
    4, 8, [0,0,1,1,1,1,1,0], [0,1,0,0,0,0,0,1], [0,1,0,0,0,0,0,1], [0,0,1,1,1,1,1,0], [0,0,0,0,0,0,0,0], # 0
    3, 8, [0,1,0,0,0,0,1,0], [0,1,1,1,1,1,1,1], [0,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # 1
    4, 8, [0,1,1,0,0,0,1,0], [0,1,0,1,0,0,0,1], [0,1,0,0,1,0,0,1], [0,1,0,0,0,1,1,0], [0,0,0,0,0,0,0,0], # 2
    4, 8, [0,0,1,0,0,0,1,0], [0,1,0,0,0,0,0,1], [0,1,0,0,1,0,0,1], [0,0,1,1,0,1,1,0], [0,0,0,0,0,0,0,0], # 3
    4, 8, [0,0,0,1,1,0,0,0], [0,0,0,1,0,1,0,0], [0,0,0,1,0,0,1,0], [0,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], # 4
    4, 8, [0,0,1,0,0,1,1,1], [0,1,0,0,0,1,0,1], [0,1,0,0,0,1,0,1], [0,0,1,1,1,0,0,1], [0,0,0,0,0,0,0,0], # 5
    4, 8, [0,0,1,1,1,1,1,0], [0,1,0,0,1,0,0,1], [0,1,0,0,1,0,0,1], [0,0,1,1,0,0,0,0], [0,0,0,0,0,0,0,0], # 6
    4, 8, [0,1,1,0,0,0,0,1], [0,0,0,1,0,0,0,1], [0,0,0,0,1,0,0,1], [0,0,0,0,0,1,1,1], [0,0,0,0,0,0,0,0], # 7
    4, 8, [0,0,1,1,0,1,1,0], [0,1,0,0,1,0,0,1], [0,1,0,0,1,0,0,1], [0,0,1,1,0,1,1,0], [0,0,0,0,0,0,0,0], # 8
    4, 8, [0,0,0,0,0,1,1,0], [0,1,0,0,1,0,0,1], [0,1,0,0,1,0,0,1], [0,0,1,1,1,1,1,0], [0,0,0,0,0,0,0,0], # 9
    2, 8, [0,1,0,1,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # :
    2, 8, [1,0,0,0,0,0,0,0], [0,1,0,1,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # ;
    3, 8, [0,0,0,1,0,0,0,0], [0,0,1,0,1,0,0,0], [0,1,0,0,0,1,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # <
    3, 8, [0,0,0,1,0,1,0,0], [0,0,0,1,0,1,0,0], [0,0,0,1,0,1,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # =
    3, 8, [0,1,0,0,0,1,0,0], [0,0,1,0,1,0,0,0], [0,0,0,1,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # >
    4, 8, [0,0,0,0,0,0,1,0], [0,1,0,1,1,0,0,1], [0,0,0,0,1,0,0,1], [0,0,0,0,0,1,1,0], [0,0,0,0,0,0,0,0], # ?
    5, 8, [0,0,1,1,1,1,1,0], [0,1,0,0,1,0,0,1], [0,1,0,1,0,1,0,1], [0,1,0,1,1,1,0,1], [0,0,0,0,1,1,1,0], # @
    4, 8, [0,1,1,1,1,1,1,0], [0,0,0,1,0,0,0,1], [0,0,0,1,0,0,0,1], [0,1,1,1,1,1,1,0], [0,0,0,0,0,0,0,0], # A
    4, 8, [0,1,1,1,1,1,1,1], [0,1,0,0,1,0,0,1], [0,1,0,0,1,0,0,1], [0,0,1,1,0,1,1,0], [0,0,0,0,0,0,0,0], # B
    4, 8, [0,0,1,1,1,1,1,0], [0,1,0,0,0,0,0,1], [0,1,0,0,0,0,0,1], [0,0,1,0,0,0,1,0], [0,0,0,0,0,0,0,0], # C
    4, 8, [0,1,1,1,1,1,1,1], [0,1,0,0,0,0,0,1], [0,1,0,0,0,0,0,1], [0,0,1,1,1,1,1,0], [0,0,0,0,0,0,0,0], # D
    4, 8, [0,1,1,1,1,1,1,1], [0,1,0,0,1,0,0,1], [0,1,0,0,1,0,0,1], [0,1,0,0,0,0,0,1], [0,0,0,0,0,0,0,0], # E
    4, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,1,0,0,1], [0,0,0,0,1,0,0,1], [0,0,0,0,0,0,0,1], [0,0,0,0,0,0,0,0], # F
    4, 8, [0,0,1,1,1,1,1,0], [0,1,0,0,0,0,0,1], [0,1,0,0,1,0,0,1], [0,1,1,1,1,0,1,0], [0,0,0,0,0,0,0,0], # G
    4, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,1,0,0,0], [0,0,0,0,1,0,0,0], [0,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], # H
    3, 8, [0,1,0,0,0,0,0,1], [0,1,1,1,1,1,1,1], [0,1,0,0,0,0,0,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # I
    4, 8, [0,0,1,1,0,0,0,0], [0,1,0,0,0,0,0,0], [0,1,0,0,0,0,0,1], [0,0,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], # J
    4, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,1,0,0,0], [0,0,0,1,0,1,0,0], [0,1,1,0,0,0,1,1], [0,0,0,0,0,0,0,0], # K
    4, 8, [0,1,1,1,1,1,1,1], [0,1,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # L
    5, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,0,0,1,0], [0,0,0,0,1,1,0,0], [0,0,0,0,0,0,1,0], [0,1,1,1,1,1,1,1], # M
    5, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,0,1,0,0], [0,0,0,0,1,0,0,0], [0,0,0,1,0,0,0,0], [0,1,1,1,1,1,1,1], # N
    4, 8, [0,0,1,1,1,1,1,0], [0,1,0,0,0,0,0,1], [0,1,0,0,0,0,0,1], [0,0,1,1,1,1,1,0], [0,0,0,0,0,0,0,0], # O
    4, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,1,0,0,1], [0,0,0,0,1,0,0,1], [0,0,0,0,0,1,1,0], [0,0,0,0,0,0,0,0], # P
    4, 8, [0,0,1,1,1,1,1,0], [0,1,0,0,0,0,0,1], [0,1,0,0,0,0,0,1], [1,0,1,1,1,1,1,0], [0,0,0,0,0,0,0,0], # Q
    4, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,1,0,0,1], [0,0,0,0,1,0,0,1], [0,1,1,1,0,1,1,0], [0,0,0,0,0,0,0,0], # R
    4, 8, [0,1,0,0,0,1,1,0], [0,1,0,0,1,0,0,1], [0,1,0,0,1,0,0,1], [0,0,1,1,0,0,1,0], [0,0,0,0,0,0,0,0], # S
    5, 8, [0,0,0,0,0,0,0,1], [0,0,0,0,0,0,0,1], [0,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,1], [0,0,0,0,0,0,0,1], # T
    4, 8, [0,0,1,1,1,1,1,1], [0,1,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], # U
    5, 8, [0,0,0,0,1,1,1,1], [0,0,1,1,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,1,1,0,0,0,0], [0,0,0,0,1,1,1,1], # V
    5, 8, [0,0,1,1,1,1,1,1], [0,1,0,0,0,0,0,0], [0,0,1,1,1,0,0,0], [0,1,0,0,0,0,0,0], [0,0,1,1,1,1,1,1], # W
    5, 8, [0,1,1,0,0,0,1,1], [0,0,0,1,0,1,0,0], [0,0,0,0,1,0,0,0], [0,0,0,1,0,1,0,0], [0,1,1,0,0,0,1,1], # X
    5, 8, [0,0,0,0,0,1,1,1], [0,0,0,0,1,0,0,0], [0,1,1,1,0,0,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,0,1,1,1], # Y
    4, 8, [0,1,1,0,0,0,0,1], [0,1,0,1,0,0,0,1], [0,1,0,0,1,0,0,1], [0,1,0,0,0,1,1,1], [0,0,0,0,0,0,0,0], # Z
    2, 8, [0,1,1,1,1,1,1,1], [0,1,0,0,0,0,0,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # [
    4, 8, [0,0,0,0,0,0,0,1], [0,0,0,0,0,1,1,0], [0,0,0,1,1,0,0,0], [0,1,1,0,0,0,0,0], [0,0,0,0,0,0,0,0], # \
    2, 8, [0,1,0,0,0,0,0,1], [0,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # ]
    3, 8, [0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,1], [0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # hat
    4, 8, [0,1,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # _
    2, 8, [0,0,0,0,0,0,0,1], [0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # `
    4, 8, [0,0,1,0,0,0,0,0], [0,1,0,1,0,1,0,0], [0,1,0,1,0,1,0,0], [0,1,1,1,1,0,0,0], [0,0,0,0,0,0,0,0], # a
    4, 8, [0,1,1,1,1,1,1,1], [0,1,0,0,0,1,0,0], [0,1,0,0,0,1,0,0], [0,0,1,1,1,0,0,0], [0,0,0,0,0,0,0,0], # b
    4, 8, [0,0,1,1,1,0,0,0], [0,1,0,0,0,1,0,0], [0,1,0,0,0,1,0,0], [0,0,1,0,1,0,0,0], [0,0,0,0,0,0,0,0], # c
    4, 8, [0,0,1,1,1,0,0,0], [0,1,0,0,0,1,0,0], [0,1,0,0,0,1,0,0], [0,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], # d
    4, 8, [0,0,1,1,1,0,0,0], [0,1,0,1,0,1,0,0], [0,1,0,1,0,1,0,0], [0,0,0,1,1,0,0,0], [0,0,0,0,0,0,0,0], # e
    3, 8, [0,0,0,0,0,1,0,0], [0,1,1,1,1,1,1,0], [0,0,0,0,0,1,0,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # f
    4, 8, [1,0,0,1,1,0,0,0], [1,0,1,0,0,1,0,0], [1,0,1,0,0,1,0,0], [0,1,1,1,1,0,0,0], [0,0,0,0,0,0,0,0], # g
    4, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,0,1,0,0], [0,0,0,0,0,1,0,0], [0,1,1,1,1,0,0,0], [0,0,0,0,0,0,0,0], # h
    3, 8, [0,1,0,0,0,1,0,0], [0,1,1,1,1,1,0,1], [0,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # i
    4, 8, [0,1,0,0,0,0,0,0], [1,0,0,0,0,0,0,0], [1,0,0,0,0,1,0,0], [0,1,1,1,1,1,0,1], [0,0,0,0,0,0,0,0], # j
    4, 8, [0,1,1,1,1,1,1,1], [0,0,0,1,0,0,0,0], [0,0,1,0,1,0,0,0], [0,1,0,0,0,1,0,0], [0,0,0,0,0,0,0,0], # k
    3, 8, [0,1,0,0,0,0,0,1], [0,1,1,1,1,1,1,1], [0,1,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # l
    5, 8, [0,1,1,1,1,1,0,0], [0,0,0,0,0,1,0,0], [0,1,1,1,1,1,0,0], [0,0,0,0,0,1,0,0], [0,1,1,1,1,0,0,0], # m
    4, 8, [0,1,1,1,1,1,0,0], [0,0,0,0,0,1,0,0], [0,0,0,0,0,1,0,0], [0,1,1,1,1,0,0,0], [0,0,0,0,0,0,0,0], # n
    4, 8, [0,0,1,1,1,0,0,0], [0,1,0,0,0,1,0,0], [0,1,0,0,0,1,0,0], [0,0,1,1,1,0,0,0], [0,0,0,0,0,0,0,0], # o
    4, 8, [1,1,1,1,1,1,0,0], [0,0,1,0,0,1,0,0], [0,0,1,0,0,1,0,0], [0,0,0,1,1,0,0,0], [0,0,0,0,0,0,0,0], # p
    4, 8, [0,0,0,1,1,0,0,0], [0,0,1,0,0,1,0,0], [0,0,1,0,0,1,0,0], [1,1,1,1,1,1,0,0], [0,0,0,0,0,0,0,0], # q
    4, 8, [0,1,1,1,1,1,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,0,1,0,0], [0,0,0,0,0,1,0,0], [0,0,0,0,0,0,0,0], # r
    4, 8, [0,1,0,0,1,0,0,0], [0,1,0,1,0,1,0,0], [0,1,0,1,0,1,0,0], [0,0,1,0,0,1,0,0], [0,0,0,0,0,0,0,0], # s
    3, 8, [0,0,0,0,0,1,0,0], [0,0,1,1,1,1,1,1], [0,1,0,0,0,1,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # t
    4, 8, [0,0,1,1,1,1,0,0], [0,1,0,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,1,1,1,1,1,0,0], [0,0,0,0,0,0,0,0], # u
    5, 8, [0,0,0,1,1,1,0,0], [0,0,1,0,0,0,0,0], [0,1,0,0,0,0,0,0], [0,0,1,0,0,0,0,0], [0,0,0,1,1,1,0,0], # v
    5, 8, [0,0,1,1,1,1,0,0], [0,1,0,0,0,0,0,0], [0,0,1,1,1,1,0,0], [0,1,0,0,0,0,0,0], [0,0,1,1,1,1,0,0], # w
    5, 8, [0,1,0,0,0,1,0,0], [0,0,1,0,1,0,0,0], [0,0,0,1,0,0,0,0], [0,0,1,0,1,0,0,0], [0,1,0,0,0,1,0,0], # x
    4, 8, [1,0,0,1,1,1,0,0], [1,0,1,0,0,0,0,0], [1,0,1,0,0,0,0,0], [0,1,1,1,1,1,0,0], [0,0,0,0,0,0,0,0], # y
    3, 8, [0,1,1,0,0,1,0,0], [0,1,0,1,0,1,0,0], [0,1,0,0,1,1,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # z
    3, 8, [0,0,0,0,1,0,0,0], [0,0,1,1,0,1,1,0], [0,1,0,0,0,0,0,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # {
    1, 8, [0,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # |
    3, 8, [0,1,0,0,0,0,0,1], [0,0,1,1,0,1,1,0], [0,0,0,0,1,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], # }
    4, 8, [0,0,0,0,1,0,0,0], [0,0,0,0,0,1,0,0], [0,0,0,0,1,0,0,0], [0,0,0,0,0,1,0,0], [0,0,0,0,0,0,0,0], # ~
]

class CharTable:

    def __init__(self, array, max_width=5, max_height=8):
        self.width = max_width
        entries_per_char = max_width + 2
        self.height = max_height
        self.dict = {}
        
        for curr_num in range(0, len(array) // entries_per_char):
            curr_char = chr(curr_num + 32)
            self.dict[curr_char] = {}
            self.dict[curr_char]["width"] = array[curr_num * entries_per_char]
            self.dict[curr_char]["height"] = array[curr_num * entries_per_char + 1]
            self.dict[curr_char]["bitmap"] = array[curr_num * entries_per_char + 2 : curr_num * entries_per_char + 2 + self.dict[curr_char]["width"]]
    
    def convert_char(self, char):
        if ord(char) < 32:
            raise Exception("Not a valid char")
        elif char not in self.dict:
            return self.dict[" "]["bitmap"]
        return self.dict[char]["bitmap"]

    def convert_string(self, string):
        array = []
        for char in string:
            array.extend(self.convert_char(char))
            array.append([0] * self.height)
        return array



class Matrix:

    def __init__(self, din_pin, cs_pin, clk_pin, height=8, modules=4, command_bits_per_module=8, data_bits_per_module=8, width_per_module=8, reg_displaytest=15, reg_scanlimit=11, reg_decodemode=9, reg_shutdown=12, reg_intensity=10):
        self.din_pin = din_pin
        self.cs_pin = cs_pin
        self.clk_pin = clk_pin
        self.height = height
        self.modules = modules
        self.command_bits_per_module = command_bits_per_module
        self.data_bits_per_module = data_bits_per_module
        self.width_per_module = width_per_module

        gpio.setup([din_pin, clk_pin], gpio.OUT, initial=0)
        gpio.setup(cs_pin, gpio.OUT, initial=0)

        for module in range(modules):
            self.send_command(self.build_command(module, reg_displaytest, 0))
            self.display_clock()
            self.send_command(self.build_command(module, reg_scanlimit, 7))
            self.display_clock()
            self.send_command(self.build_command(module, reg_decodemode, 0))
            self.display_clock()
            self.send_command(self.build_command(module, reg_intensity, 7))
            self.display_clock()
            self.send_command(self.build_command(module, reg_shutdown, 1))
            self.display_clock()
    
        self.current_output = [[0] * self.height] * (self.modules * self.width_per_module)
        self.output_buffer = queue.Queue() # variable length
        # self.current_output = [[0 for i in range(height)] for i in range(width)] # column-major

    def add_string(self, string, char_table):
        converted = char_table.convert_string(string)
        for col in converted:
            self.output_buffer.put(col)

    def add_blank_space(self, length=None):
        if length == None:
            length = self.width_per_module * self.modules
        space = [[0] * self.height] * length
        for col in space:
            self.output_buffer.put(col)

    def render(self):
        for mod in range(self.modules):
            start = mod * self.width_per_module
            end = (mod + 1) * self.width_per_module
            for alt in range(self.height - 1, -1, -1):
                self.send_command(self.build_command(mod, 8 - alt, [self.current_output[i][alt] for i in range(start, end)]))
                self.display_clock()

    def shift_to_current_output(self):
        for col in range(len(self.current_output) - 1):
            self.current_output[col] = self.current_output[col + 1]
        self.current_output[-1] = self.output_buffer.get()

    def build_command(self, module, command_half, data_half):
        if type(command_half) == int:
            command_half = num_to_bits(command_half)
        while len(command_half) < self.command_bits_per_module:
            command_half.insert(0, 0)
        if type(data_half) == int:
            data_half = num_to_bits(data_half)
        while len(data_half) < self.data_bits_per_module:
            data_half.insert(0, 0)
        
        command = [0] * module * (self.command_bits_per_module + self.data_bits_per_module)
        command.extend(command_half)
        command.extend(data_half)
        while len(command) < self.modules * (self.command_bits_per_module + self.data_bits_per_module):
            command.append(0)
        return command

    def bit_push(self, bit):
        gpio.output(self.din_pin, bit)
        gpio.output(self.clk_pin, 1)
        gpio.output(self.clk_pin, 0)

    def send_command(self, arr):
        for bit in arr:
            self.bit_push(bit)

    def display_clock(self):
        gpio.output(self.cs_pin, 1)
        gpio.output(self.cs_pin, 0)

    def print_current_output(self):
        print("-" * len(self.current_output))
        for alt in range(self.height - 1, -1, -1):
            print("|", end="")
            for col in range(len(self.current_output)):
                print("@" if self.current_output[col][alt] == 1 else ".", end="")
            print("|")
        print("-" * len(self.current_output))

    def print_output_buffer(self):
        print("-" * len(self.output_buffer))
        for alt in range(self.height - 1, -1, -1):
            print("|", end="")
            for col in range(len(self.output_buffer)):
                print("@" if self.output_buffer[col][alt] == 1 else ".", end="")
            print("|")
        print("-" * len(self.output_buffer))

class BouncyBall:

    def __init__(self, width=32, height=8, startpos = [0, 0], startdir = [1, 1]):
        self.width = width
        self.height = height
        self.curr_pos = startpos
        self.curr_dir = startdir

    def get_display(self):
        output = [[0 for i in range(self.height)] for j in range(self.width)]
        output[self.curr_pos[0]][self.curr_pos[1]] = 1
        return output

    def next_state(self):
        new_pos = [self.curr_pos[0] + self.curr_dir[0], self.curr_pos[1] + self.curr_dir[1]]
        if new_pos[0] not in range(self.width):
            self.curr_dir[0] *= -1
            new_pos[0] = self.curr_pos[0] + self.curr_dir[0]
        if new_pos[1] not in range(self.height):
            self.curr_dir[1] *= -1
            new_pos[1] = self.curr_pos[1] + self.curr_dir[1]
        self.curr_pos = new_pos



def num_to_bits(num):
    return [1 if digit=='1' else 0 for digit in bin(num)[2:]]

    
def run_repeat_text(string="lorem ipsum"):
    gpio.setmode(gpio.BOARD)

    chartable = CharTable(chars)
    ball = BouncyBall()
    matrix = Matrix(11, 13, 15)

    try:
        while True:
            matrix.add_string(string, chartable)
            matrix.add_blank_space()
            while not matrix.output_buffer.empty():
                time.sleep(0.0125)
                matrix.shift_to_current_output()
                # print(matrix.output_buffer.qsize())
                matrix.print_current_output()
                # matrix.print_output_buffer()
                matrix.render()
    except KeyboardInterrupt:
        gpio.cleanup()


def run_bouncy_ball(string):
    gpio.setmode(gpio.BOARD)

    ball = BouncyBall()
    matrix = Matrix(11, 13, 15)

    try:
        while True:
            matrix.current_output = ball.get_display()
            matrix.print_current_output()
            matrix.render()
            ball.next_state()
            time.sleep(0.05)
    except KeyboardInterrupt:
        gpio.cleanup()


def run_repeat_text_web(url):
    gpio.setmode(gpio.BOARD)

    chartable = CharTable(chars)
    matrix = Matrix(11, 13, 15)

    string = requests.get(url).text

    try:
        while True:
            matrix.add_string(string, chartable)
            matrix.add_blank_space()
            while not matrix.output_buffer.empty():
                time.sleep(0.0125)
                matrix.shift_to_current_output()
                # print(matrix.output_buffer.qsize())
                matrix.print_current_output()
                # matrix.print_output_buffer()
                matrix.render()
    except KeyboardInterrupt:
        gpio.cleanup()

def run_repeat_datetime():
    gpio.setmode(gpio.BOARD)

    chartable = CharTable(chars)
    matrix = Matrix(11, 13, 15)

    try:
        while True:
            matrix.add_string(get_datetime(), chartable)
            matrix.add_blank_space()
            while not matrix.output_buffer.empty():
                time.sleep(0.0125)
                matrix.shift_to_current_output()
                # print(matrix.output_buffer.qsize())
                matrix.print_current_output()
                # matrix.print_output_buffer()
                matrix.render()
    except KeyboardInterrupt:
        gpio.cleanup()

def run_repeat_weather():
    gpio.setmode(gpio.BOARD)

    chartable = CharTable(chars)
    matrix = Matrix(11, 13, 15)

    try:
        while True:
            matrix.add_string(get_weather(), chartable)
            matrix.add_blank_space()
            while not matrix.output_buffer.empty():
                time.sleep(0.0125)
                matrix.shift_to_current_output()
                # print(matrix.output_buffer.qsize())
                matrix.print_current_output()
                # matrix.print_output_buffer()
                matrix.render()
    except KeyboardInterrupt:
        gpio.cleanup()

def run_repeat_headlines():
    gpio.setmode(gpio.BOARD)

    chartable = CharTable(chars)
    matrix = Matrix(11, 13, 15)

    headline_queue = queue.Queue()

    try:
        while True:
            new_headlines = get_headlines()
            for i in new_headlines:
                headline_queue.put(i)
            while not headline_queue.empty():
                headline = headline_queue.get()
                try:
                    matrix.add_string(" | ".join(headline), chartable)
                    matrix.add_blank_space()
                    while not matrix.output_buffer.empty():
                        time.sleep(0.02)
                        matrix.shift_to_current_output()
                        # print(matrix.output_buffer.qsize())
                        matrix.print_current_output()
                        # matrix.print_output_buffer()
                        matrix.render()
                except:
                    pass
                
            
    except KeyboardInterrupt:
        gpio.cleanup()

def get_headlines():
    with open('headline_key.txt', 'rt') as hkey:
        api_key = hkey.read()

    response = requests.get("http://newsapi.org/v2/top-headlines?country=us&apiKey={}".format(api_key)).json()
    # print(response)

    headlines = [(i["title"], i["description"]) for i in response["articles"]]
    return headlines



def get_weather(city_name="new york"):
    with open('weather_key.txt', 'rt') as wkey:
        api_key = wkey.read()

    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=imperial".format(city_name, api_key)).json()

    formal_name = response["name"]
    desc = response["weather"][0]["description"]
    temp = response["main"]["temp"]
    feels_like = response["main"]["feels_like"]
    low = response["main"]["temp_min"]
    high = response["main"]["temp_max"]
    humidity = response["main"]["humidity"]
    wind_speed = response["wind"]["speed"]
    wind_deg = response["wind"]["deg"]

    return "The weather in {} is {}. The temperature is {} F and it feels like {} F. The low is {} F and the high is {} F. The humidity is {}%. The wind speed is {} mph at {} degrees.".format(formal_name, desc, temp, feels_like, low, high, humidity, wind_speed, wind_deg)

    

def get_sports(team_list):
    pass

def get_stocks(symbol_list):
    pass

def get_datetime():
    now = datetime.datetime.now()
    return now.strftime("Today is %A, %B %d, %Y. The time is %I:%M %p.")

    

        
