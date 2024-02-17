""" Somewhat nicer wrapper around ot_api.runs for health related things """

from ot_api.requestor import get as rget, post

def get():
  return rget("/health")

def home():
  return post("/robot/home", data={"target": "robot"})

